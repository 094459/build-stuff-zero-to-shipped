"""
BorrowRequest model for the book sharing application.
"""
from datetime import datetime

from src.extensions import db

class BorrowRequest(db.Model):
    __tablename__ = 'borrow_requests'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, denied
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requester = db.relationship('User', backref=db.backref('borrow_requests', lazy='dynamic'))
    
    def __init__(self, book_id, requester_id):
        self.book_id = book_id
        self.requester_id = requester_id
        
    def __repr__(self):
        return f'<BorrowRequest {self.request_id}>'
        
    def approve(self):
        self.status = 'approved'
        
    def deny(self):
        self.status = 'denied'