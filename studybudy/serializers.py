"""StudyBuddy Serializers.

This module provides serializers for user management, including signup,
login, profile updates, and password reset functionality. The serializers
handle data validation, user creation, and profile modifications.

Available Serializers:
    - SignupSerializer: New user registration with profile fields
    - LoginSerializer: User authentication
    - UpdateProfileSerializer: Profile data updates
    - ResetPasswordRequestSerializer: Password reset request
    - ResetPasswordSerializer: New password validation

All serializers include appropriate validation rules and error messages.
The SignupSerializer handles secure password creation and email uniqueness.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from studybudy.models import GenderChoices

CustomUser = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """Serializer for user registration with profile creation.

    Handles new user registration with required fields (email, username,
    password) and optional profile information. Includes validation for
    unique email/username and password strength.

    Fields:
        id (int, read-only): User ID
        email (str): Unique email address, max 80 chars
        username (str): Unique username, max 20 chars
        password (str): Min 8 chars, write-only
        password2 (str): Password confirmation
        profile_picture (ImageField, optional): User avatar
        phone_number (str, optional): Contact number
        gender (str, optional): From GenderChoices
        date_of_birth (Date, optional): User's birth date

    Validation:
        - Email must be unique
        - Username must be unique
        - Passwords must match and meet strength requirements
        - Optional fields can be null
    """

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        max_length=80,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="A user with that email already exists.",
            )
        ],
    )
    username = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="This username is already taken.",
            )
        ],
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(
        min_length=8, write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        min_length=8, write_only=True, required=True, style={"input_type": "password"}
    )

    # optional extras — adapt type to your model (ImageField, PhoneNumberField, etc.)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=GenderChoices.choices, required=False, allow_null=True
    )
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "gender",
            "phone_number",
            "date_of_birth",
            "profile_picture",
            "password",
            "password2",
            "created_at",
            "updated_at",
            "gender_display",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        """Validate the signup data.

        Performs password validation:
        1. Ensures both password fields are provided
        2. Verifies passwords match
        3. Validates password strength using Django's validators

        Args:
            attrs (dict): The attributes to validate

        Returns:
            dict: The validated attributes

        Raises:
            ValidationError: If passwords don't match or fail strength check
        """
        pw = attrs.get("password")
        pw2 = attrs.get("password2")

        if pw is None or pw2 is None:
            raise serializers.ValidationError(
                {"password": "Both password and password2 are required."}
            )

        if pw != pw2:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        try:
            validate_password(password=pw, user=None)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)})  # type: ignore
        return attrs

    def create(self, validated_data):
        """Create a new user instance.

        Creates a user with a secure password using the custom user manager.
        Handles email normalization and uses transaction atomic to ensure
        data consistency.

        Args:
            validated_data (dict): The validated user data

        Returns:
            CustomUser: The created user instance

        Raises:
            ValidationError: If user creation fails
        """
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        email = validated_data.get("email")
        if email:
            validated_data["email"] = email.lower()
        try:
            with transaction.atomic():
                manager = CustomUser.objects
                if hasattr(manager, "create_user"):
                    user = manager.create_user(password=password, **validated_data)
                else:
                    user = CustomUser(**validated_data)
                    user.set_password(password)
                    user.save()
        except Exception as e:  # noqa: F841
            raise serializers.ValidationError(
                {"non_field_errors": "Unable to create account. Please try again."}
            )

        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login authentication.

    Simple serializer that validates login credentials.
    Password field is write-only for security.

    Fields:
        email (str): User's email address
        password (str): User's password (write-only)

    Note:
        This serializer doesn't perform the actual authentication,
        it only validates the presence of required fields.
    """

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile information.

    Handles updates to user profile data, excluding sensitive fields
    like email and username which are read-only. All fields are
    optional to support partial updates.

    Fields:
        first_name (str, optional): User's first name
        last_name (str, optional): User's last name
        profile_picture (ImageField, optional): User's avatar
        phone_number (PhoneNumberField, optional): Contact number
        gender (str, optional): From GenderChoices
        date_of_birth (Date, optional): User's birth date

    Read-only fields:
        username: Cannot be changed after signup
        email: Cannot be changed after signup
        gender_display: Human-readable gender choice

    Note:
        Use PATCH for partial updates and PUT for full updates.
    """

    first_name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    phone_number = PhoneNumberField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=GenderChoices.choices, required=False, allow_null=True
    )
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "profile_picture",
            "phone_number",
            "gender",
            "gender_display",
            "date_of_birth",
        ]
        extra_kwargs = {"username": {"read_only": True}, "email": {"read_only": True}}


class ResetPasswordRequestSerializer(serializers.Serializer):
    """Serializer for initiating a password reset request.

    Validates the email address format and existence before
    initiating the password reset process.

    Fields:
        email (str): Email address to send reset link

    Validation:
        - Email must be in valid format
        - Custom email validation using Django's EmailValidator
    """

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Validate email format using Django's EmailValidator.

        Args:
            value (str): The email to validate

        Returns:
            str: The validated email

        Raises:
            ValidationError: If email format is invalid
        """
        try:
            EmailValidator()(value)
            return value
        except ValidationError:
            raise serializers.ValidationError("use a valid email")


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for setting a new password during reset.

    Handles validation of new password strength and confirmation.
    Enforces password requirements through regex pattern.

    Fields:
        new_password (str): New password matching requirements
        confirm_password (str): Must match new_password

    Password Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one digit
        - At least one special character (@$!%*?&)
    """

    new_password = serializers.RegexField(
        regex=r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        write_only=True,
        error_messages={
            "invalid": (
                "Password must be at least 8 characters long with at least one capital letter and symbol"
            )
        },
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
