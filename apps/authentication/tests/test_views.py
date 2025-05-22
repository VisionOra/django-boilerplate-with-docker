"""
Tests for authentication views.

This module contains test cases for the authentication views, ensuring proper
functionality of user registration, profile management, and email account operations.
"""

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRegisterView:
    """Test the RegisterView."""

    def test_register_user_success(self, api_client):
        """Test successful user registration."""
        url = reverse("register")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPassword123!",
            "password2": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "access" in response.data
        assert "refresh" in response.data
        assert "user" in response.data
        assert response.data["user"]["email"] == data["email"]

    def test_register_user_password_mismatch(self, api_client):
        """Test user registration with mismatched passwords."""
        url = reverse("register")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPassword123!",
            "password2": "DifferentPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data


@pytest.mark.django_db
class TestUserProfileView:
    """Test the UserProfileView."""

    def test_get_profile(self, auth_client):
        """Test getting user profile."""
        url = reverse("user-profile")

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_update_profile(self, auth_client):
        """Test updating user profile."""
        url = reverse("user-profile")
        data = {"bio": "Updated bio", "company": "Test Company", "job_title": "Test Job"}

        response = auth_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["bio"] == data["bio"]
        assert response.data["company"] == data["company"]
        assert response.data["job_title"] == data["job_title"]


@pytest.mark.django_db
class TestEmailAccountView:
    """Test the EmailAccountView."""

    def test_add_email_account(self, auth_client):
        """Test adding an email account."""
        url = reverse("email-accounts")
        data = {
            "email": "test@gmail.com",
            "provider": "gmail",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "imap_server": "imap.gmail.com",
            "imap_port": 993,
            "use_tls": True,
        }

        response = auth_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "email" in response.data
        assert response.data["email"] == data["email"]

    def test_remove_email_account(self, auth_client):
        """Test removing an email account."""
        # First add an email account
        add_url = reverse("email-accounts")
        email = "test@gmail.com"
        add_data = {
            "email": email,
            "provider": "gmail",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "imap_server": "imap.gmail.com",
            "imap_port": 993,
            "use_tls": True,
        }
        auth_client.post(add_url, add_data, format="json")

        # Then remove it
        remove_url = reverse("email-account-detail", kwargs={"email_id": email})
        response = auth_client.delete(remove_url)

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data
