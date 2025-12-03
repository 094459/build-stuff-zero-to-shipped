# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.src.extensions import db, login_manager
from app.src.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
