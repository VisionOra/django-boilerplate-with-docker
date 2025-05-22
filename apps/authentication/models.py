"""
Models for user authentication and profile management.

This module contains models and signals for managing user profiles and
authentication-related functionality.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserProfile(models.Model):
    """
    Extended user profile model to store additional user information
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email_signature = models.TextField(blank=True, null=True)
    email_accounts = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="JSON field to store connected email accounts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class for the UserProfile model."""

        app_label = "authentication"

    def __str__(self):
        """Return a string representation of the user profile."""
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a user profile when a new user is created
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the user profile when the user is saved
    """
    instance.profile.save()
