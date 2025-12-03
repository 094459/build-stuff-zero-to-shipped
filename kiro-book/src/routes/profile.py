"""
User profile routes for the book sharing application.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from src.extensions import db
from src.models import User, Book, BorrowRequest, BorrowingHistory
from src.forms.profile import ProfileForm

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def index():
    """Display current user's profile."""
    return render_template('profile/index.html', user=current_user)

@profile_bp.route('/edit', methods=['POST'])
@login_required
def edit():
    """Edit current user's profile."""
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.alias = form.alias.data
        current_user.bio = form.bio.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.index'))
    
    return render_template('profile/edit.html', form=form)

@profile_bp.route('/edit', methods=['GET'])
@login_required
def edit_get():
    """Display form to edit current user's profile."""
    form = ProfileForm(obj=current_user)
    return render_template('profile/edit.html', form=form)

@profile_bp.route('/books')
@login_required
def books():
    """Display books owned by the current user."""
    # Using join to eagerly load borrower information
    user_books = Book.query.filter_by(owner_id=current_user.user_id).all()
    return render_template('profile/books.html', books=user_books)

@profile_bp.route('/borrowed')
@login_required
def borrowed():
    """Display books currently borrowed by the user."""
    borrowed_books = Book.query.filter_by(current_borrower_id=current_user.user_id).all()
    return render_template('profile/borrowed.html', books=borrowed_books)

@profile_bp.route('/history')
@login_required
def history():
    """Display borrowing history for the current user - both borrowed and lent books."""
    # Books the user has borrowed from others
    borrowed_history = BorrowingHistory.query.filter_by(borrower_id=current_user.user_id).all()
    
    # Books the user has lent to others (books owned by the user that have been borrowed)
    lent_history = BorrowingHistory.query.join(Book).filter(Book.owner_id == current_user.user_id).all()
    
    return render_template('profile/history.html', 
                          borrowed_history=borrowed_history,
                          lent_history=lent_history)

@profile_bp.route('/requests')
@login_required
def requests():
    """Display borrow requests made by and to the current user."""
    # Requests made by the current user
    outgoing_requests = BorrowRequest.query.filter_by(requester_id=current_user.user_id).all()
    
    # Requests for books owned by the current user
    incoming_requests = BorrowRequest.query.join(Book).filter(
        Book.owner_id == current_user.user_id,
        BorrowRequest.status == 'pending'
    ).all()
    
    return render_template('profile/requests.html', 
                          outgoing_requests=outgoing_requests,
                          incoming_requests=incoming_requests)

@profile_bp.route('/invite')
@login_required
def invite():
    """Display the user's invite code."""
    return render_template('profile/invite.html', invite_code=current_user.personal_invite_code)

@profile_bp.route('/<int:user_id>')
def view(user_id):
    """View another user's profile."""
    user = User.query.get_or_404(user_id)
    
    # Get public books owned by this user
    public_books = Book.query.filter_by(owner_id=user_id, is_available=True).all()
    
    return render_template('profile/view.html', user=user, books=public_books)