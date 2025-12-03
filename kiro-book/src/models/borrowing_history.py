"""
BorrowingHistory model for the book sharing application.
"""
from datetime import datetime

from src.extensions import db

class BorrowingHistory(db.Model):
    __tablename__ = 'borrowing_history'
    
    borrow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    
    # Relationship with borrower
    borrower = db.relationship('User', backref=db.backref('borrowing_history', lazy='dynamic'))
    
    def __init__(self, book_id, borrower_id):
        self.book_id = book_id
        self.borrower_id = borrower_id
        
    def __repr__(self):
        return f'<BorrowingHistory {self.borrow_id}>'
        
    def mark_returned(self):
        from datetime import timezone
        self.return_date = datetime.now(timezone.utc)