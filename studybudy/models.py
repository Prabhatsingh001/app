"""studybudy.models

This module defines the project's custom user model and its manager.

Classes
- CustomUserManager: Manager that creates regular users and superusers using
    email as the unique identifier.
- CustomUser: Custom user model that extends Django's AbstractUser to use an
    email-based login and store additional profile fields (phone number,
    date of birth, profile picture, etc.).

Notes
- The project sets `AUTH_USER_MODEL = 'studybudy.CustomUser'` in
    `app/settings.py`. The manager's `create_user` and `create_superuser`
    methods are intended to be used by create commands and tests.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date

class CustomUserManager(BaseUserManager):
    """Manager for CustomUser.

    Provides helper methods to create regular users and superusers where
    the email field is used as the USERNAME_FIELD.
    """

    def create_user(self, email, password, **extra_fields):
        """Create and return a user with the given email and password.

        Args:
            email (str): The user's email address (required).
            password (str): Plain-text password for the new user.
            **extra_fields: Additional model fields for the user.

        Returns:
            CustomUser: The saved user instance.

        Raises:
            ValueError: If `email` is not provided.
        """
        if not email:
            raise ValueError(_("Email Should be Provided"))
        email = self.normalize_email(email)
        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new_user.save()
        return new_user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a superuser.

        Ensures the created user has `is_staff`, `is_superuser` and
        `is_active` set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("super user should have is_staff as True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("super user should have is_superuser as True"))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("super user should have is_active as True"))
        return self.create_user(email, password, **extra_fields)
    
class GenderChoices(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'

class CustomUser(AbstractUser):
    """Custom user model.

    Extends Django's AbstractUser but uses `email` as the unique
    identifier (login field). Additional profile fields are provided
    such as `phone_number`, `date_of_birth` and `profile_picture`.

    Important attributes:
    - USERNAME_FIELD = 'email'  # login field
    - REQUIRED_FIELDS = ['username']  # required when creating superusers
    """

    email = models.EmailField(_("your Email"), unique=True, max_length=80)
    username = models.CharField(_("username"), max_length=20, unique=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, default=GenderChoices.OTHER)
    phone_number = PhoneNumberField(null=True, blank=True)
    date_of_birth = models.DateField(default=date(1999, 10, 19), null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()  # type: ignore

    def __str__(self):
        """Return a compact string representation for debugging/logging."""
        return f"<{self.email}>"

