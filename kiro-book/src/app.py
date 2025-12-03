"""
Main application factory for the book sharing application.
"""
import os
from flask import Flask
from pathlib import Path

from src.extensions import db, login_manager, migrate, csrf
from src.models import User, Book, BookComment, BorrowingHistory, InviteCode, BookUpvote, BorrowRequest

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists with absolute path
    instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
    os.makedirs(instance_path, exist_ok=True)
    
    # Database file path with absolute path
    db_path = os.path.join(instance_path, 'bookshare.db')
    
    # Configure the app
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Register blueprints
    from src.routes.main import main_bp
    from src.routes.auth import auth_bp
    from src.routes.books import books_bp
    from src.routes.profile import profile_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(profile_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create initial invite code if none exists
        if not InviteCode.query.first():
            # Create a special system user for the initial invite code
            system_user = User.query.filter_by(email="system@bookshare.app").first()
            if not system_user:
                system_user = User(
                    email="system@bookshare.app",
                    password=os.urandom(24).hex(),  # Random secure password
                    alias="System",
                    invite_code_used="SYSTEM"
                )
                db.session.add(system_user)
                db.session.commit()
            
            # Create the initial invite code with the system user as creator
            initial_code = InviteCode(invite_code='INITIAL', creator_id=system_user.user_id)
            db.session.add(initial_code)
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    #app.run(debug=True)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=5000)