#!/home/ubuntu/flask_app/venv/bin/python3
import sys
import logging
from pathlib import Path

# Activate virtual environment
activate_this = '/home/ubuntu/flask_app/venv/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

# Define the path to the Flask app
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import the app from the Flask app
from app import app as application

# Optional: Log errors to Apache
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)