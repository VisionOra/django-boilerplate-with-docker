# flake8: noqa
"""
    This file is used to load the correct settings for the environment.
    It will load the settings for the environment specified in the ENV_NAME variable.
    If the ENV_NAME variable is not set, it will load the development settings.
"""

import os

from dotenv import load_dotenv

# Load environment variables before importing settings
BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)
env_name = os.environ.get("ENV_NAME", ".env")
env_path = os.path.join(BASE_DIR, env_name)
load_dotenv(env_path)
print(f"\n\nLoading environment variables from {env_path}")


# Determine which settings module to use
environment = os.environ.get("DJANGO_ENVIRONMENT", "development")

if environment == "staging":
    from .staging import *
else:
    from .development import *

print(f"Using {environment} settings")
