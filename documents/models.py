"""Models for uploaded documents and search metadata."""

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils import timezone


def document_upload_to(instance, filename):
    """Build the upload path for a document file."""

    return f"documents/{instance.uploader_id}/{timezone.now().strftime('%Y/%m')}/{filename}"


class DocumentCategory(models.IntegerChoices):
    """Available document categories."""

    NOTE = 1, "note"
    QUESTION_PAPER = 2, "question_paper"
    SLIDE = 3, "slide"
    ASSIGNMENT = 4, "assignment"


class Document(models.Model):
    """Store a document uploaded by a user."""

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documents",
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_upload_to)
    category = models.IntegerField(
        choices=DocumentCategory.choices, default=DocumentCategory.NOTE
    )
    course = models.CharField(max_length=128, blank=True, null=True)
    subject = models.CharField(max_length=128, blank=True, null=True)
    sem = models.PositiveSmallIntegerField(default=1)
    tags = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)
    views = models.PositiveIntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)
    ocr_text = models.TextField(blank=True)  # OCRed text / extracted text
    search_vector = SearchVectorField(
        null=True, blank=True
    )  # Postgres tsvector storage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database indexes for document search."""

        indexes = [
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self):
        """Return the document title."""

        return self.title
