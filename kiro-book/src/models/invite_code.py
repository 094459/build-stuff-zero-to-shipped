"""
InviteCode model for the book sharing application.
"""
from datetime import datetime

from src.extensions import db

class InviteCode(db.Model):
    __tablename__ = 'invite_codes'
    
    invite_code = db.Column(db.String(20), primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    times_used = db.Column(db.Integer, nullable=False, default=0)  # Track usage count
    
    def __init__(self, invite_code, creator_id):
        self.invite_code = invite_code
        self.creator_id = creator_id
        
    def __repr__(self):
        return f'<InviteCode {self.invite_code}>'
        
    def use_code(self):
        """Mark the code as used and deactivate if it's the initial code."""
        self.times_used += 1
        # If this is the initial code, deactivate after first use
        if self.invite_code == 'INITIAL' and self.times_used >= 1:
            self.is_active = False
