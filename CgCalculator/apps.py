"""Application configuration for the CGPA calculator app."""

from django.apps import AppConfig


class CgcalculatorConfig(AppConfig):
    """Register the CGPA calculator app with Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "CgCalculator"
