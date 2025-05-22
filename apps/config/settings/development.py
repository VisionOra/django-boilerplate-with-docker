# flake8: noqa
"""
Development settings for email marketing project.
"""

import os

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "email_marketing"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Email settings - Use console backend for development
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
# EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
# EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
# DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@example.com")

# Mailgun settings
# MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", "")
# MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", "artilence.tech")

# Celery settings
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# AI Service settings
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8000")
AI_SERVICE_API_KEY = os.getenv("AI_SERVICE_API_KEY", "default-key-for-dev")

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Disable security features that are not needed in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to access the cookie in development
CSRF_COOKIE_SAMESITE = None  # Disable SameSite restriction in development
SESSION_COOKIE_SAMESITE = None  # Disable SameSite restriction in development
CSRF_USE_SESSIONS = False  # Don't store CSRF in the session
CSRF_COOKIE_DOMAIN = None  # No domain restriction in development

# Override security headers for development
SECURE_CROSS_ORIGIN_OPENER_POLICY = None  # Disable COOP for development
SECURE_REFERRER_POLICY = "same-origin"
