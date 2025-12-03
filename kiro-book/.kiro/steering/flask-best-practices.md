---
inclusion: always
---

# Flask 3.0 Development Guidelines

Use Flask 3.0 for web application development with modern Python best practices.

## Application Factory Pattern

Always use the application factory pattern for creating Flask apps:

```python
from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    from extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from routes.api import api_bp
    from routes.main import main_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)
    
    return app
```

## Project Structure

Use this standard project layout:

```
├── app/
│   ├── __init__.py
│   ├── extensions.py          # Extension instances (db, migrate, etc.)
│   ├── config.py              # Configuration classes
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py             # API blueprint
│   │   └── main.py            # Main blueprint
│   ├── services/              # Business logic layer
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── schemas/               # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   └── user_schema.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       └── base.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
├── migrations/                # Alembic migrations
├── .env.example
├── pyproject.toml
└── run.py                     # Application entry point
```

## Configuration Management

Use environment variables and configuration classes:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

## Extensions Setup

Initialize extensions in a separate file to avoid circular imports:

```python
# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
```

## Blueprint Organization

Organize routes using blueprints:

```python
# routes/api.py
from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from schemas.user_schema import UserCreateSchema
from services.user_service import UserService

api_bp = Blueprint('api', __name__)

@api_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = UserCreateSchema(**request.get_json())
        user = UserService.create_user(data)
        return jsonify(user.to_dict()), 201
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
```

## Data Validation with Pydantic

Use Pydantic for request/response validation:

```python
# schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True
```

## Database Models

Define models with proper relationships and methods:

```python
# models/user.py
from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
```

## Service Layer Pattern

Separate business logic from routes:

```python
# services/user_service.py
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def create_user(data):
        user = User(
            username=data.username,
            email=data.email,
            password_hash=generate_password_hash(data.password)
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get_or_404(user_id)
    
    @staticmethod
    def get_all_users():
        return User.query.all()
```

## Error Handling

Implement global error handlers:

```python
# In create_app()
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(ValidationError)
def validation_error(error):
    return jsonify({'errors': error.errors()}), 400
```

## Testing

Write tests using pytest and fixtures:

```python
# tests/conftest.py
import pytest
from app import create_app
from extensions import db
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# tests/test_api.py
def test_create_user(client):
    response = client.post('/api/users', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['username'] == 'testuser'
```

## Application Entry Point

Create a simple entry point:

```python
# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
```

## Package Management

Use uv for all dependency management:

```bash
# Install dependencies
uv add flask flask-sqlalchemy flask-migrate pydantic[email] python-dotenv

# Development dependencies
uv add --dev pytest pytest-flask ruff black

# Run the application
uv run python run.py

# Run tests
uv run pytest
```

## Best Practices

- Always use blueprints for route organization
- Separate business logic into service classes
- Use Pydantic for data validation
- Implement proper error handling
- Use environment variables for configuration
- Write tests for all endpoints
- Use type hints throughout the codebase
- Follow PEP 8 style guidelines
- Use database migrations for schema changes
- Never commit sensitive data or .env files
- Use context managers for database operations
- Implement proper logging
- Use Flask's built-in security features (CSRF, secure cookies)
