"""Application configuration for the feedback app."""

from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """Register the feedback app with Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
