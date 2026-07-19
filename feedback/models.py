"""Models for document feedback and ratings."""

from django.conf import settings
from django.db import models

from documents.models import Document


class FeedbackChoices(models.IntegerChoices):
    """Available rating values for feedback."""

    ONE = 1, "1"
    TWO = 2, "2"
    THREE = 3, "3"
    FOUR = 4, "4"
    FIVE = 5, "5"


class Feedback(models.Model):
    """Store a user's rating and comment for a document."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="feedback",
        null=True,
        blank=True,
    )
    document = models.ForeignKey(
        Document, related_name="feedbacks", on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(
        choices=FeedbackChoices.choices, null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Default ordering for feedback entries."""

        ordering = ("-created_at",)

    def __str__(self):
        """Return a short summary of the feedback entry."""

        return f"Feedback by {self.user.username if self.user else 'Anonymous'} - {self.rating} Stars"
