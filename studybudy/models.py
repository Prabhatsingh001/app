"""Models for the StudyBuddy user and profile data."""

from datetime import date

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """Manager for creating StudyBuddy users."""

    def create_user(self, email, password, **extra_fields):
        """Create and return a regular user.

        Args:
            email: User email address.
            password: Plain-text password for the new account.
            **extra_fields: Additional model fields.

        Returns:
            CustomUser: The created user instance.

        Raises:
            ValueError: If email is not provided.
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

        Ensures the created user has staff, superuser, and active flags set.
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
    """Available gender choices for user profiles."""

    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHER = "O", "Other"


class CustomUser(AbstractUser):
    """Custom user model that authenticates by email."""

    email = models.EmailField(_("your Email"), unique=True, max_length=80)
    username = models.CharField(_("username"), max_length=20, unique=True)
    gender = models.CharField(
        max_length=1, choices=GenderChoices.choices, default=GenderChoices.OTHER
    )
    phone_number = PhoneNumberField(null=True, blank=True)
    date_of_birth = models.DateField(default=date(1999, 10, 19), null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()  # type: ignore

    def __str__(self):
        """Return the user email for display and debugging."""

        return f"<{self.email}>"


class Profile(models.Model):
    """Additional profile information linked to a user."""

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    roll_number = models.CharField(max_length=64, blank=True, null=True)
    course = models.CharField(max_length=128, null=True, blank=True)
    sem = models.PositiveIntegerField(default=1)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        """Return a human-readable profile label."""

        return f"{self.user.username} profile"
