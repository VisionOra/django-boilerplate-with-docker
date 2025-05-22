"""
Admin configuration for authentication models.

This module provides admin interface configurations for user-related models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
