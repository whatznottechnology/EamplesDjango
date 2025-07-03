import os
import sys

# Add your project directory to the sys.path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Create logs directory if it doesn't exist
logs_dir = os.path.join(project_dir, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Set environment variable to tell Django where your settings.py is
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'examples.production_settings')

# Set up Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 