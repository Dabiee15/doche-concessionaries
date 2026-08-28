"""
WSGI config for doche_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doche_project.settings')
django.setup()

# Self-healing: Run migrations and collectstatic automatically on Gunicorn boot
try:
    from django.core.management import call_command
    print("Running self-healing database migrations...")
    call_command('migrate', interactive=False)
    print("Running self-healing collectstatic...")
    call_command('collectstatic', interactive=False, clear=True)
    print("Self-healing deployment tasks completed successfully!")
except Exception as e:
    print(f"Self-healing error (ignoring): {e}")

application = get_wsgi_application()
app = application

