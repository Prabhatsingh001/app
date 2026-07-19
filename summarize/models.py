"""Models for stored text summaries."""

from django.db import models


class summarize_model(models.Model):
    """Store an original text and its summary."""

    text = models.TextField()
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the original text for display."""

        return self.text
