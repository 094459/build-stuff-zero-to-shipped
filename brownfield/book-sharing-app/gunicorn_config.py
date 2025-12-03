"""
Gunicorn configuration file for the Book Sharing Application.
"""
import os
import multiprocessing

# Bind to 0.0.0.0:8000 by default
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')

# Number of worker processes
workers = os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1)

# Worker class - use gevent for better performance
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'gevent')

# Timeout in seconds
timeout = os.environ.get('GUNICORN_TIMEOUT', 30)

# Log level
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')

# Access log file
accesslog = os.environ.get('GUNICORN_ACCESS_LOG', '-')

# Error log file
errorlog = os.environ.get('GUNICORN_ERROR_LOG', '-')

# Process name
proc_name = os.environ.get('GUNICORN_PROC_NAME', 'book-sharing-app')

# Preload application code before forking workers
preload_app = True

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

# Graceful timeout
graceful_timeout = 30
