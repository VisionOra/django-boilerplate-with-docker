"""
Create a Django management command to create a superuser with
username 'admin' and password 'admin'.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to create an admin user."""

    help = "Creates a superuser with username 'admin' and password 'admin'"

    def handle(self, *args, **options):
        """Create a superuser with username 'admin' and password 'admin'."""
        User = get_user_model()
        if User.objects.filter(username="admin").exists():
            self.stdout.write(self.style.WARNING("Admin user already exists"))
            return

        User.objects.create_superuser(username="admin", email="admin@example.com", password="admin")
        self.stdout.write(
            self.style.SUCCESS("Successfully created superuser with username 'admin'")
        )
