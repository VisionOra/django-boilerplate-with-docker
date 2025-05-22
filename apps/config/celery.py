"""
Celery configuration file.
"""

import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.config.settings")

# Get Redis URL from environment and ensure it's set for Celery
redis_url = os.environ.get("REDIS_URL")
if redis_url:
    os.environ["CELERY_BROKER_URL"] = redis_url
    os.environ["CELERY_RESULT_BACKEND"] = redis_url
    print(f"Using Redis URL from environment: {redis_url}")
else:
    print("WARNING: REDIS_URL environment variable not found!")

app = Celery("email_marketing")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Debug task to print the request."""
    print(f"Request: {self.request!r}")
