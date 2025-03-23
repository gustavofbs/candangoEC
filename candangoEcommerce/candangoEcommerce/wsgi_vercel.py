import os
import sys

# Add the project directory to the sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candangoEcommerce.candangoEcommerce.settings')

from django.core.wsgi import get_wsgi_application

# Get the Django WSGI application
application = get_wsgi_application()

# Wrap the Django WSGI application with WhiteNoise
from whitenoise import WhiteNoise
application = WhiteNoise(application)

# Add this for Vercel
app = application
