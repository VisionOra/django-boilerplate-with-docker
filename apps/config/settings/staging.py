# flake8: noqa
"""
Staging settings for email marketing project.
"""

import os
from ipaddress import IPv4Network

from .base import *  # noqa

print("Starting staging settings")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# Add our custom middleware at the beginning of the MIDDLEWARE list
MIDDLEWARE = [
    "apps.appsUtils.middleware.AllowInternalIPsMiddleware",  # Custom middleware to handle AWS health checks
] + MIDDLEWARE

# Create a list of allowed hosts
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "10.0.0.0/16",  # VPC CIDR range - covers all internal IPs
    "*.artilence.tech",  # Allow all subdomains
    "*.artilence.com",
    "api.artilence.com",
    "artilence.com",
    "artilence-portfolio-alb-1234567890.us-east-1.elb.amazonaws.com",  # ALB domain
    "54.157.97.192",  # ALB IP
    "34.230.183.220",  # ALB IP
    "10.0.1.39",  # Adding specific IPs for clarity
    "10.0.1.64",
    "10.0.2.140",
    "10.0.2.161",
    "10.0.2.176",
    "10.0.2.202",
    "0.0.0.0",
]

# Add specific IPs that have been encountered in health checks
# Explicitly expanding the CIDR range to catch all possible IPs used for health checks
vpc_network = IPv4Network("10.0.0.0/16")
for subnet in [
    IPv4Network("10.0.1.0/24"),
    IPv4Network("10.0.2.0/24"),
]:
    # Only add IPs that are not already in the ALLOWED_HOSTS
    ALLOWED_HOSTS.extend([str(ip) for ip in subnet.hosts() if str(ip) not in ALLOWED_HOSTS])

print(f"Expanded ALLOWED_HOSTS count: {len(ALLOWED_HOSTS)}")

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "email-marketing"),
        "USER": os.environ.get("DB_USER", "email-marketing-postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "email-marketing-postgres"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

print(f"DB_HOST: {DATABASES}")
# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@example.com")

# Mailgun settings
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", "artilence.tech")

# Celery settings
redis_url = os.environ.get("REDIS_URL")
print(f"REDIS_URL from environment: {redis_url}")

CELERY_BROKER_URL = redis_url or os.environ.get(
    "CELERY_BROKER_URL",
    "redis://artilence-portfolio-redis.fysci1.0001.use1.cache.amazonaws.com:6379/0",
)
CELERY_RESULT_BACKEND = redis_url or os.environ.get(
    "CELERY_RESULT_BACKEND",
    "redis://artilence-portfolio-redis.fysci1.0001.use1.cache.amazonaws.com:6379/0",
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# AI Service settings
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://ai-service:8000")
AI_SERVICE_API_KEY = os.getenv("AI_SERVICE_API_KEY")

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://api.artilence.com",
    "https://artilence.com",
    "https://*.artilence.com",
    "https://*.artilence.tech",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "https://api.artilence.com",
    "https://artilence.com",
    "https://*.artilence.com",
    "https://*.artilence.tech",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://10.0.2.176",  # ALB IP
]

# Security settings
SECURE_SSL_REDIRECT = os.environ.get(
    "SECURE_SSL_REDIRECT", "False"
)  # Let the load balancer handle SSL
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_COOKIE_DOMAIN = os.environ.get("CSRF_COOKIE_DOMAIN", None)
CSRF_COOKIE_SAMESITE = os.environ.get("CSRF_COOKIE_SAMESITE", None)
SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE", None)
CSRF_USE_SESSIONS = os.environ.get("CSRF_USE_SESSIONS", False)
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", False)
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", False)
CSRF_COOKIE_HTTPONLY = os.environ.get("CSRF_COOKIE_HTTPONLY", False)


# Security headers
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"  # Less restrictive COOP setting
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = None  # Disable COEP in staging for compatibility
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

print(f"CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"CORS_ALLOW_CREDENTIALS: {CORS_ALLOW_CREDENTIALS}")
print(f"CORS_ALLOW_ALL_ORIGINS: {CORS_ALLOW_ALL_ORIGINS}")
print(f"CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")
print(f"CSRF_COOKIE_DOMAIN: {CSRF_COOKIE_DOMAIN}")
print(f"SECURE_CROSS_ORIGIN_OPENER_POLICY: {SECURE_CROSS_ORIGIN_OPENER_POLICY}")
