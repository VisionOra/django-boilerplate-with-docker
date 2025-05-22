"""
Views for user authentication and profile management.

This module contains views for handling user registration, profile management,
and email account operations.
"""

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    EmailAccountSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserSerializer,
)
from .models import User

UserModel = get_user_model()


@extend_schema(
    summary="Get CSRF token",
    description="Fetch a new CSRF token for making POST requests",
    tags=["authentication"],
    responses={200: {"properties": {"csrfToken": {"type": "string"}}}},
)
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Returns CSRF token required for making POST requests to the API.

    This endpoint sets a CSRF cookie and returns the token value
    in the response body for the client to use in X-CSRFToken header.

    Args:
        request: The HTTP request object

    Returns:
        JsonResponse: A JSON object containing the CSRF token
    """
    token = get_token(request)
    return JsonResponse({"csrfToken": token})


@extend_schema_view(
    post=extend_schema(
        summary="Register a new user",
        description="Create a new user account and return JWT tokens",
        tags=["authentication"],
        responses={201: UserSerializer},
    )
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    get=extend_schema(
        summary="Get user profile",
        description="Retrieve the current user's profile information",
        tags=["authentication"],
    ),
    put=extend_schema(
        summary="Update user profile",
        description="Update the current user's profile information",
        tags=["authentication"],
    ),
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@extend_schema_view(
    post=extend_schema(
        summary="Add email account",
        description="Connect a new email account to the user's profile",
        tags=["authentication"],
    ),
    delete=extend_schema(
        summary="Remove email account",
        description="Remove an email account from the user's profile",
        tags=["authentication"],
        parameters=[
            OpenApiParameter(
                name="email_id", description="Email address to remove", required=True, type=str
            )
        ],
    ),
)
class EmailAccountView(APIView):
    """
    API view to manage connected email accounts
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Add a new email account to the user's profile.

        Args:
            request: The HTTP request object containing email account data

        Returns:
            Response: Success message on success, or validation errors
        """
        serializer = EmailAccountSerializer(data=request.data)
        if serializer.is_valid():
            email_data = serializer.validated_data
            user_profile = request.user.profile

            # Add the new email account to the user's email accounts
            if not user_profile.email_accounts:
                user_profile.email_accounts = {}

            email_id = email_data.get("email")
            user_profile.email_accounts[email_id] = {
                "provider": email_data.get("provider"),
                "smtp_server": email_data.get("smtp_server"),
                "smtp_port": email_data.get("smtp_port"),
                "imap_server": email_data.get("imap_server"),
                "imap_port": email_data.get("imap_port"),
                "use_tls": email_data.get("use_tls", True),
                "is_active": True,
            }
            user_profile.save()

            return Response(
                {"message": "Email account added successfully", "email": email_id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email_id=None):
        """
        Remove an email account from the user's profile.

        Args:
            request: The HTTP request object
            email_id: The email address to remove

        Returns:
            Response: Success message on success, or error message on failure
        """
        if not email_id:
            return Response({"error": "Email ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = request.user.profile
        if user_profile.email_accounts and email_id in user_profile.email_accounts:
            # Remove the email account
            user_profile.email_accounts.pop(email_id)
            user_profile.save()
            return Response({"message": "Email account removed successfully"})
        else:
            return Response({"error": "Email account not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary="Get user data",
    description="Retrieve the current user's data including profile details",
    tags=["authentication"],
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_data(request):
    """
    Retrieve user data and profile details.

    Args:
        request: The HTTP request object

    Returns:
        Response: User data and profile details
    """
    user = request.user
    user_data = UserSerializer(user).data
    profile_data = UserProfileSerializer(user.profile).data

    return Response({"user": user_data, "profile": profile_data})
