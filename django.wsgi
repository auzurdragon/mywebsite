import os
import sys

# import django.core.handlers.wsgi

from django.conf import settings

from django.core.wsgi import get_wsgi_application

# Add this file path to sys.path in oreder to import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

os.environ['DJANGO_SETTINGS_MODLE'] = 'mywebsite.settings'

sys.stdout = sys.stderr

DEBUG = True
# application =django.core.handlers.wsgi.WSGIHandler()
application = get_wsgi_application()
