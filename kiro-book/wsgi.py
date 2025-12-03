"""
WSGI entry point for the Book Sharing Application.
This file is used by Gunicorn to serve the application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.app import create_app

# Create the application instance
application = create_app()

# For compatibility with some WSGI servers that look for 'app'
app = application

if __name__ == '__main__':
    application.run()
