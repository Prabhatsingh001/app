"""Application configuration for the notes and question paper app."""

from django.apps import AppConfig


class UploadnotesorquestionpaperConfig(AppConfig):
    """Register the notes and question paper app with Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "UploadNotesOrQuestionPaper"
