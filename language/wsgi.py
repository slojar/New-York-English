"""
WSGI config for datacore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

if config('env', '') == 'prod' or os.getenv('env', 'dev') == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language.settings.dev')


application = get_wsgi_application()
