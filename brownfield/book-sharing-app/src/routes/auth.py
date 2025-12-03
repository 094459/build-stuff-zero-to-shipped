"""
Authentication routes for the book sharing application.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from src.extensions import db
from src.models import User, InviteCode
from src.forms.auth import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if invite code is valid
        invite_code = InviteCode.query.filter_by(
            invite_code=form.invite_code.data, 
            is_active=True
        ).first()
        
        if not invite_code:
            flash('Invalid or expired invite code.', 'danger')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            email=form.email.data,
            password=form.password.data,
            alias=form.alias.data,
            invite_code_used=form.invite_code.data
        )
        
        # Add user to database and commit to get the user_id
        db.session.add(user)
        db.session.commit()
        
        # Now create personal invite code with the user's ID
        personal_invite = InviteCode(
            invite_code=user.personal_invite_code,
            creator_id=user.user_id
        )
        
        # Mark the invite code as used
        invite_code.use_code()
        if invite_code.creator_id != 0:  # Skip for initial invite code
            creator = User.query.get(invite_code.creator_id)
            if creator:
                creator.invites_used_count += 1
        
        db.session.add(personal_invite)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/register', methods=['GET'])
def register_get():
    """User registration page (GET method)."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # Use url_for to generate safe URLs and validate the next_page
            if next_page:
                # Validate that next_page is a relative path
                if not next_page.startswith('/'):
                    next_page = '/'
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/login', methods=['GET'])
def login_get():
    """User login page (GET method)."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))