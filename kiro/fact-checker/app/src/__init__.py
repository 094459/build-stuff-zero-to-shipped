# SPDX-License-Identifier: Apache-2.0
# (C)opyright 2025 BeachGeek.co.uk

from flask import Flask
from app.src.extensions import db, login_manager
from app.src.routes import auth, main, facts, categories
import os


def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///factchecker.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(facts.bp)
    app.register_blueprint(categories.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
