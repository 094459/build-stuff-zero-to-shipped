"""
Main routes for the book sharing application.
"""
from flask import Blueprint, render_template, request, current_app
from sqlalchemy import desc

from src.models import Book

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Display the dashboard with all books and available books."""
    page = request.args.get('page', 1, type=int)
    view_type = request.args.get('view', 'all')  # Default to all books
    category = request.args.get('category', 'all')  # Default to all categories
    per_page = 10
    
    # Base query - exclude hidden books from all dashboard views
    base_query = Book.query.filter_by(is_hidden=False)
    
    # Apply category filter if specified
    if category == 'fiction':
        base_query = base_query.filter_by(is_fiction=True)
    elif category == 'non-fiction':
        base_query = base_query.filter_by(is_fiction=False)
    
    # Get books, sorted by creation date (newest first)
    if view_type == 'available':
        # Get only available books
        books = base_query.filter_by(is_available=True).order_by(desc(Book.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        active_tab = 'available'
    else:
        # Get all books (except hidden ones)
        books = base_query.order_by(desc(Book.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        active_tab = 'all'
    
    return render_template('index.html', books=books, active_tab=active_tab, active_category=category)
