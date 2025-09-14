"""
WSGI config for ANUMC Django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""
from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application  # type: ignore

# Set the default settings module for the 'django' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anumc_website.settings")

application = get_wsgi_application()