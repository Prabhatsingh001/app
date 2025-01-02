from rest_framework import serializers
from .models import Notes, QuestionPaper

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'sem', 'title', 'file', 'created_at', 'updated_at']  
        read_only_fields = ['created_at', 'updated_at']
        
    def validate_file(self, value):
        if not value.name.endswith(('.pdf', '.doc', '.docx')):
            raise serializers.ValidationError("Only .pdf, .doc, and .docx files are allowed.")
        return value
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value


class QuestionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPaper
        fields = ['id', 'sem', 'title', 'file', 'created_at', 'updated_at']  
        read_only_fields = ['created_at', 'updated_at']
        
    def validate_file(self, value):
        if not value.name.endswith(('.pdf')):
            raise serializers.ValidationError("Only .pdf files are allowed.")
        return value
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
