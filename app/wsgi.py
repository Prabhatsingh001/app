"""WSGI entrypoint for the app project.

This module exposes the WSGI callable used by synchronous servers.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = get_wsgi_application()
