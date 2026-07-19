"""Models for uploaded notes and question papers."""

from django.conf import settings
from django.db import models


class SemChoices(models.IntegerChoices):
    """Available semester values."""

    SEM1 = 1, "sem1"
    SEM2 = 2, "sem2"
    SEM3 = 3, "sem3"
    SEM4 = 4, "sem4"
    SEM5 = 5, "sem5"
    SEM6 = 6, "sem6"
    SEM7 = 7, "sem7"
    SEM8 = 8, "sem8"


class Notes(models.Model):
    """Store a note uploaded by a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sem = models.IntegerField(default=SemChoices.SEM1, choices=SemChoices.choices)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to="notes/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the note title."""

        return self.title


class QuestionPaper(models.Model):
    """Store a question paper uploaded by a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sem = models.IntegerField(default=SemChoices.SEM1, choices=SemChoices.choices)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to="question_papers/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the question paper title."""

        return self.title
