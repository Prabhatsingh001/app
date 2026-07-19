"""Admin configuration for uploaded notes and question papers."""

from django.contrib import admin

from .models import Notes, QuestionPaper

admin.site.register(Notes)
admin.site.register(QuestionPaper)
