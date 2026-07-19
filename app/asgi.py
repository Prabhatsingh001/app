"""ASGI entrypoint for the app project.

This module exposes the ASGI callable used by asynchronous servers.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = get_asgi_application()
