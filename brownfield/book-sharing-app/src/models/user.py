"""
User model for the book sharing application.
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

from src.extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    invite_code_used = db.Column(db.String(20), nullable=False)
    personal_invite_code = db.Column(db.String(20), unique=True, nullable=False)
    invites_used_count = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationships
    books = db.relationship('Book', backref='owner', lazy='dynamic', 
                           foreign_keys='Book.owner_id')
    borrowed_books = db.relationship('Book', backref='borrower', lazy='dynamic',
                                    foreign_keys='Book.current_borrower_id')
    comments = db.relationship('BookComment', backref='user', lazy='dynamic')
    invite_codes = db.relationship('InviteCode', backref='creator', lazy='dynamic')
    
    def __init__(self, email, password, alias, invite_code_used):
        self.email = email
        self.set_password(password)
        self.alias = alias
        self.invite_code_used = invite_code_used
        self.personal_invite_code = self.generate_invite_code()
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_invite_code(self):
        return secrets.token_urlsafe(8)
    
    def get_id(self):
        return str(self.user_id)
    
    def __repr__(self):
        return f'<User {self.email}>'