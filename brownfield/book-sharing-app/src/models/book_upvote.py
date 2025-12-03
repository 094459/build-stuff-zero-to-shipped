"""
BookUpvote model for the book sharing application.
"""
from datetime import datetime

from src.extensions import db

class BookUpvote(db.Model):
    __tablename__ = 'book_upvotes'
    
    upvote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('book_id', 'user_id', name='uq_book_user_upvote'),
    )
    
    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id
        
    def __repr__(self):
        return f'<BookUpvote {self.upvote_id}>'