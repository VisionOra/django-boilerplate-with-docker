"""
Django app configuration for authentication.

This module configures the authentication app and its settings.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    App configuration for the authentication app.

    Handles the configuration and initialization of the authentication app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"
