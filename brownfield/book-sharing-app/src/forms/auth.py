"""
Authentication forms for the book sharing application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from src.models import User, InviteCode

class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    alias = StringField('Display Name', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    invite_code = StringField('Invite Code', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        """Validate that the email is not already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')
    
    def validate_invite_code(self, invite_code):
        """Validate that the invite code exists and is active."""
        code = InviteCode.query.filter_by(invite_code=invite_code.data).first()
        if not code:
            raise ValidationError('Invalid invite code.')
        if not code.is_active:
            raise ValidationError('This invite code is no longer active.')