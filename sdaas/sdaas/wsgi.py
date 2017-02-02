"""
WSGI config for sdaas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ubuntu/public/sdaas.nl/sdaas')
sys.path.append('/home/ubuntu/public/sdaas.nl/sdaas/sdaas')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sdaas.settings.production")

application = get_wsgi_application()
