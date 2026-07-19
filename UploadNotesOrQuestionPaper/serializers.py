"""Serializers for notes and question paper uploads."""

from rest_framework import serializers

from .models import Notes, QuestionPaper


class NotesSerializer(serializers.ModelSerializer):
    """Validate uploaded notes."""

    class Meta:
        """Serializer metadata for notes."""

        model = Notes
        fields = ["id", "sem", "title", "file", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_file(self, value):
        """Ensure the note file uses an allowed document extension."""

        if not value.name.endswith((".pdf", ".doc", ".docx")):
            raise serializers.ValidationError(
                "Only .pdf, .doc, and .docx files are allowed."
            )
        return value

    def validate_title(self, value):
        """Ensure the note title is long enough."""

        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value


class QuestionPaperSerializer(serializers.ModelSerializer):
    """Validate uploaded question papers."""

    class Meta:
        """Serializer metadata for question papers."""

        model = QuestionPaper
        fields = ["id", "sem", "title", "file", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_file(self, value):
        """Ensure the question paper file is a PDF."""

        if not value.name.endswith((".pdf")):
            raise serializers.ValidationError("Only .pdf files are allowed.")
        return value

    def validate_title(self, value):
        """Ensure the question paper title is long enough."""

        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value
