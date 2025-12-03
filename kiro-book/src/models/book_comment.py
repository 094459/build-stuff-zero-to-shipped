"""
BookComment model for the book sharing application.
"""
from datetime import datetime

from src.extensions import db

class BookComment(db.Model):
    __tablename__ = 'book_comments'
    
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, book_id, user_id, comment_text):
        self.book_id = book_id
        self.user_id = user_id
        self.comment_text = comment_text
        
    def __repr__(self):
        return f'<BookComment {self.comment_id}>'