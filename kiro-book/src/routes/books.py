"""
Book management routes for the book sharing application.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import desc

from src.extensions import db, csrf
from src.models import Book, BookComment, BookUpvote, BorrowRequest, BorrowingHistory
from src.forms.book import BookForm, CommentForm, BorrowRequestForm

books_bp = Blueprint('books', __name__, url_prefix='/books')

# amazonq-ignore-next-line
@books_bp.route('/')
def index():
    """Display all books."""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Exclude hidden books from the general book listing
    books = Book.query.filter_by(is_hidden=False).order_by(desc(Book.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('books/index.html', books=books)

# Import the necessary modules for authorization
from flask_login import login_required
from flask import abort

@books_bp.route('/<int:book_id>')
@login_required  # Ensures only authenticated users can access this route
def view(book_id):
    """Display a single book."""

    book = Book.query.get_or_404(book_id)
    comments = BookComment.query.filter_by(book_id=book_id).order_by(BookComment.created_at).all()
    comment_form = CommentForm()
    borrow_form = BorrowRequestForm()
    
    # Check if current user has upvoted this book
    user_upvoted = False
    if current_user.is_authenticated:
        user_upvoted = book.is_upvoted_by(current_user.user_id)
    
    # Check if current user has a pending borrow request
    pending_request = None
    if current_user.is_authenticated:
        pending_request = BorrowRequest.query.filter_by(
            book_id=book_id,
            requester_id=current_user.user_id,
            status='pending'
        ).first()
    
    return render_template(
        'books/view.html',
        book=book,
        comments=comments,
        comment_form=comment_form,
        borrow_form=borrow_form,
        user_upvoted=user_upvoted,
        pending_request=pending_request
    )

@books_bp.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new book."""
    form = BookForm()
    
    if form.validate_on_submit():
        book = Book(
            owner_id=current_user.user_id,
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            purchase_url=form.purchase_url.data,
            recommendation_rating=form.recommendation_rating.data
        )
        
        # Set hidden status if specified
        book.is_hidden = form.is_hidden.data
        
        # Set fiction/non-fiction status
        book.is_fiction = form.is_fiction.data == 'fiction'
        
        db.session.add(book)
        db.session.commit()
        
        flash('Book created successfully!', 'success')
        return redirect(url_for('books.view', book_id=book.book_id))
    
    return render_template('books/create.html', form=form)

@books_bp.route('/create', methods=['GET'])
@login_required
def create_get():
    """Display the book creation form."""
    form = BookForm()
    return render_template('books/create.html', form=form)

@books_bp.route('/<int:book_id>/edit', methods=['POST'])
@login_required
def edit(book_id):
    """Edit an existing book."""
    book = Book.query.get_or_404(book_id)
    
    # Check if current user is the owner
    if book.owner_id != current_user.user_id:
        abort(403)
    
    form = BookForm(obj=book)
    if form.validate_on_submit():
        # Update most fields using form data
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.purchase_url = form.purchase_url.data
        book.recommendation_rating = form.recommendation_rating.data
        book.is_hidden = form.is_hidden.data
        
        # Convert the fiction/non-fiction string to boolean
        book.is_fiction = form.is_fiction.data == 'fiction'
        
        db.session.commit()
        
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.view', book_id=book.book_id))
    
    return render_template('books/edit.html', form=form, book=book)

@books_bp.route('/<int:book_id>/edit', methods=['GET'])
@login_required
def edit_get(book_id):
    """Display the edit form for an existing book."""
    book = Book.query.get_or_404(book_id)
    
    # Check if current user is the owner
    if book.owner_id != current_user.user_id:
        abort(403)
    
    form = BookForm(obj=book)
    return render_template('books/edit.html', form=form, book=book)

@books_bp.route('/<int:book_id>/toggle-visibility', methods=['POST'])
@login_required
@csrf.exempt
def toggle_visibility(book_id):
    """Toggle the visibility of a book."""
    book = Book.query.get_or_404(book_id)
    
    # Check if current user is the owner
    if book.owner_id != current_user.user_id:
        abort(403)
    
    # Toggle the hidden status
    book.is_hidden = not book.is_hidden
    db.session.commit()
    
    status = "hidden from" if book.is_hidden else "visible on"
    flash(f'"{book.title}" is now {status} public dashboards.', 'success')
    return redirect(url_for('profile.books'))

@books_bp.route('/<int:book_id>/comment', methods=['POST'])
@login_required
def add_comment(book_id):
    """Add a comment to a book."""
    book = Book.query.get_or_404(book_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = BookComment(
            book_id=book_id,
            user_id=current_user.user_id,
            comment_text=form.comment_text.data
        )
        db.session.add(comment)
        db.session.commit()
        
        flash('Comment added successfully!', 'success')
    
    return redirect(url_for('books.view', book_id=book_id))

@books_bp.route('/<int:book_id>/upvote', methods=['POST'])
@login_required
def toggle_upvote(book_id):
    """Toggle upvote for a book."""
    book = Book.query.get_or_404(book_id)
    
    # Toggle the upvote
    is_upvoted = book.toggle_upvote(current_user.user_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return {'upvoted': is_upvoted, 'count': book.upvote_count}
    
    return redirect(url_for('books.view', book_id=book_id))

@books_bp.route('/<int:book_id>/borrow', methods=['POST'])
@login_required
def request_borrow(book_id):
    """Request to borrow a book."""
    book = Book.query.get_or_404(book_id)
    
    # Check if book is available
    if not book.is_available:
        flash('This book is not available for borrowing.', 'danger')
        return redirect(url_for('books.view', book_id=book_id))
    
    # Check if user is not the owner
    if book.owner_id == current_user.user_id:
        flash('You cannot borrow your own book.', 'danger')
        return redirect(url_for('books.view', book_id=book_id))
    
    # Check if user already has a pending request
    existing_request = BorrowRequest.query.filter_by(
        book_id=book_id,
        requester_id=current_user.user_id,
        status='pending'
    ).first()
    
    if existing_request:
        flash('You already have a pending request for this book.', 'warning')
        return redirect(url_for('books.view', book_id=book_id))
    
    # Create a new borrow request
    borrow_request = BorrowRequest(
        book_id=book_id,
        requester_id=current_user.user_id
    )
    db.session.add(borrow_request)
    db.session.commit()
    
    flash('Borrow request submitted successfully!', 'success')
    return redirect(url_for('books.view', book_id=book_id))

@books_bp.route('/requests/<int:request_id>/approve', methods=['POST'])
@login_required
def approve_request(request_id):
    """Approve a borrow request."""
    borrow_request = BorrowRequest.query.get_or_404(request_id)
    book = Book.query.get_or_404(borrow_request.book_id)
    
    # Check if current user is the owner of the book
    if book.owner_id != current_user.user_id:
        abort(403)
    
    # Check if book is still available
    if not book.is_available:
        flash('This book is no longer available for borrowing.', 'danger')
        return redirect(url_for('profile.requests'))
    
    # Update the book status
    book.is_available = False
    book.current_borrower_id = borrow_request.requester_id
    
    # Update the request status
    borrow_request.status = 'approved'
    
    # Create a borrowing history record
    history = BorrowingHistory(
        book_id=book.book_id,
        borrower_id=borrow_request.requester_id
    )
    db.session.add(history)
    
    # Reject all other pending requests for this book
    other_requests = BorrowRequest.query.filter_by(
        book_id=book.book_id,
        status='pending'
    ).filter(BorrowRequest.request_id != request_id).all()
    
    for request in other_requests:
        request.status = 'rejected'
    
    db.session.commit()
    
    flash('Borrow request approved successfully!', 'success')
    return redirect(url_for('profile.requests'))

@books_bp.route('/requests/<int:request_id>/reject', methods=['POST'])
@login_required
def reject_request(request_id):
    """Reject a borrow request."""
    borrow_request = BorrowRequest.query.get_or_404(request_id)
    book = Book.query.get_or_404(borrow_request.book_id)
    
    # Check if current user is the owner of the book
    if book.owner_id != current_user.user_id:
        abort(403)
    
    # Update the request status
    borrow_request.status = 'rejected'
    db.session.commit()
    
    flash('Borrow request rejected.', 'success')
    return redirect(url_for('profile.requests'))

@books_bp.route('/<int:book_id>/return', methods=['POST'])
@login_required
def return_book(book_id):
    """Return a borrowed book."""
    book = Book.query.get_or_404(book_id)
    
    # Check if current user is the borrower
    if book.current_borrower_id != current_user.user_id:
        abort(403)
    
    # Update the book status
    book.is_available = True
    
    # Update the borrowing history
    history = BorrowingHistory.query.filter_by(
        book_id=book_id,
        borrower_id=current_user.user_id,
        return_date=None
    ).first()
    
    if history:
        history.mark_returned()
    
    # Clear the current borrower
    book.current_borrower_id = None
    
    db.session.commit()
    
    flash('Book returned successfully!', 'success')
    return redirect(url_for('profile.borrowed'))
