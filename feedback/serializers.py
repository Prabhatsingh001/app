"""Serializers for feedback submissions and listings."""

from rest_framework import serializers

from .models import Feedback, FeedbackChoices


class FeedbackSerializer(serializers.ModelSerializer):
    """Validate feedback comments and ratings."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comment = serializers.CharField(max_length=200)
    rating = serializers.ChoiceField(choices=FeedbackChoices.choices)

    class Meta:
        """Serializer metadata for feedback records."""

        model = Feedback
        fields = ["id", "comment", "rating", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_rating(self, value):
        """Ensure the rating is within the supported range."""

        if value not in [1, 2, 3, 4, 5]:
            raise serializers.ValidationError("rating must be between 1 and 5")
        return value

    def validate_comment(self, value):
        """Ensure the comment length stays within the field limit."""

        if value.length > 200:
            raise serializers.ValidationError("comment exceeds 200 word limit")
        return value
