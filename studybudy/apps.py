"""Application configuration for the StudyBuddy app."""

from django.apps import AppConfig


class StudybudyConfig(AppConfig):
    """Register the StudyBuddy app and its startup hooks."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "studybudy"

    def ready(self):
        """Import signal handlers when Django starts the app."""

        import studybudy.signals  # noqa: F401
