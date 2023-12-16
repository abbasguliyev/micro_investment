"""
WSGI config for micro_investment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from micro_investment.settings.base import DEBUG

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'micro_investment.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'micro_investment.settings.prod')

application = get_wsgi_application()
