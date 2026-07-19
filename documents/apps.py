"""Application configuration for the documents app."""

from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    """Register the documents app with Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "documents"
