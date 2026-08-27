import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doche_project.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app='core';")
    print("Cleared core from django_migrations table.")
