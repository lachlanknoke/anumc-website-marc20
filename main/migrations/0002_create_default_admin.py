"""Create a default admin user for the ANUMC site.

This migration ensures that a superuser with username ``username`` and
password ``password`` exists.  If the user already exists, it is
left unchanged.
"""

from django.db import migrations
from django.contrib.auth import get_user_model


def create_default_admin(apps, schema_editor) -> None:
    User = get_user_model()
    username = "username"
    password = "password"
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email="", password=password)


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_default_admin)]