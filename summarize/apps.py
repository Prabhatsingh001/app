"""Application configuration for the summarize app."""

from django.apps import AppConfig


class SummarizeConfig(AppConfig):
    """Register the summarize app with Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "summarize"
