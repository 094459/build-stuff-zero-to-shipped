"""
Entry point for the Book Sharing Application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.app import create_app

app = create_app()

if __name__ == '__main__':
    # Use port 5001 instead of the default 5000 to avoid conflicts with AirPlay on macOS
    # app.run(debug=True, port=5000)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=5000)
