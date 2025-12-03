"""
Book model for the book sharing application.
"""
from datetime import datetime

from src.extensions import db
from src.models.book_upvote import BookUpvote

class Book(db.Model):
    __tablename__ = 'books'
    
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), nullable=True)
    purchase_url = db.Column(db.String(512), nullable=True)
    recommendation_rating = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    is_hidden = db.Column(db.Boolean, nullable=False, default=False)
    is_fiction = db.Column(db.Boolean, nullable=False, default=True)
    current_borrower_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('BookComment', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    upvotes = db.relationship('BookUpvote', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    borrow_requests = db.relationship('BorrowRequest', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    borrowing_history = db.relationship('BorrowingHistory', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, owner_id, title, author, recommendation_rating, isbn=None, purchase_url=None, is_fiction=True):
        self.owner_id = owner_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.purchase_url = purchase_url
        self.recommendation_rating = recommendation_rating
        self.is_available = True
        self.is_hidden = False
        self.is_fiction = is_fiction
        
    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
        
    @property
    def upvote_count(self):
        return self.upvotes.count()
        
    def is_upvoted_by(self, user_id):
        return self.upvotes.filter_by(user_id=user_id).first() is not None
        
    def toggle_upvote(self, user_id):
        existing_upvote = self.upvotes.filter_by(user_id=user_id).first()
        if existing_upvote:
            db.session.delete(existing_upvote)
            db.session.commit()
            return False
        else:
            new_upvote = BookUpvote(book_id=self.book_id, user_id=user_id)
            db.session.add(new_upvote)
            db.session.commit()
            return True