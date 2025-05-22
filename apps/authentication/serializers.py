"""
Serializers for user authentication and profile management.

This module contains serializers for handling user registration, profile updates,
and email account management.
"""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        """
        Meta class for UserSerializer.

        Defines the model and fields for user serialization.
        """

        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """

    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        """
        Meta class for UserProfileSerializer.

        Defines the model and fields for user profile serialization.
        """

        model = UserProfile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "company_name",
            "phone_number",
            "email_signature",
            "email_accounts",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "email", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        """
        Update a user profile instance with validated data.

        Args:
            instance: The UserProfile instance to update
            validated_data: The validated data to update with

        Returns:
            The updated UserProfile instance
        """
        # Handle user data separately
        user_data = validated_data.pop("user", {})
        if user_data:
            user = instance.user
            user.first_name = user_data.get("first_name", user.first_name)
            user.last_name = user_data.get("last_name", user.last_name)
            user.save()

        # Update profile data
        instance.company_name = validated_data.get("company_name", instance.company_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.email_signature = validated_data.get("email_signature", instance.email_signature)

        if "email_accounts" in validated_data:
            instance.email_accounts = validated_data.get("email_accounts")

        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        Meta class for RegisterSerializer.

        Defines the model and fields for user registration.
        """

        model = User
        fields = ["username", "password", "password2", "email", "first_name", "last_name"]

    def validate(self, attrs):
        """
        Validate that the passwords match.

        Args:
            attrs: The attributes to validate

        Returns:
            The validated attributes

        Raises:
            ValidationError: If passwords don't match
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user with the validated data.

        Args:
            validated_data: The validated data to create the user with

        Returns:
            The created User instance
        """
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class EmailAccountSerializer(serializers.Serializer):
    """
    Serializer for email account connection
    """

    email = serializers.EmailField(required=True)
    provider = serializers.CharField(max_length=50, required=True)
    smtp_server = serializers.CharField(max_length=255, required=True)
    smtp_port = serializers.IntegerField(required=True)
    imap_server = serializers.CharField(max_length=255, required=True)
    imap_port = serializers.IntegerField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    use_tls = serializers.BooleanField(default=True)

    def validate(self, attrs):
        """
        Validate the email account credentials.

        Args:
            attrs: The attributes to validate

        Returns:
            The validated attributes
        """
        # Here you might want to validate the connection to the email server
        # before accepting the credentials
        return attrs
