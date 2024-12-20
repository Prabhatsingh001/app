from rest_framework import serializers
from .models import Notes

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        
    def validate_file(self, value):
        if not value.name.endswith(('.pdf', '.doc', '.docx')):
            raise serializers.ValidationError("Only .pdf, .doc, and .docx files are allowed.")
        return value
