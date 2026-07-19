"""Serializers for CGPA and SGPA calculations."""

from rest_framework import serializers


class SGPAInputSerializer(serializers.Serializer):
    """Validate a single semester's SGPA and credit values."""

    sgpa = serializers.FloatField(
        error_messages={
            "required": "SGPA is required.",
            "invalid": "SGPA must be a number.",
        }
    )
    credits = serializers.IntegerField(
        error_messages={
            "required": "Credits are required.",
            "invalid": "Credits must be an integer.",
        }
    )

    def validate_sgpa(self, value):
        """Ensure the SGPA is within the valid 0 to 10 range."""

        if value < 0 or value > 10:
            raise serializers.ValidationError("SGPA must be between 0 and 10.")
        return value

    def validate_credits(self, value):
        """Ensure credits are a positive integer."""

        if value <= 0:
            raise serializers.ValidationError("Credits must be a positive integer.")
        return value


class CGPACalculatorSerializer(serializers.Serializer):
    """Validate the input payload for CGPA calculation."""

    semesters = serializers.ListField(
        child=SGPAInputSerializer(),
        allow_empty=False,
        error_messages={
            "required": "The 'semesters' field is required.",
            "blank": "The 'semesters' field cannot be blank.",
        },
    )


class CompletedSemesterSerializer(serializers.Serializer):
    """Represent a completed semester in the required SGPA payload."""

    sgpa = serializers.FloatField()
    credits = serializers.IntegerField()


class RequiredSGPASerializer(serializers.Serializer):
    """Validate the input payload for required SGPA calculations."""

    completed_semesters = serializers.ListField(child=CompletedSemesterSerializer())
    total_program_credits = serializers.IntegerField()
    future_semester_credits = serializers.IntegerField()
    expected_cgpa = serializers.FloatField()
