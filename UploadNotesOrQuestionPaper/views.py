from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Notes,QuestionPaper
from .serializers import NotesSerializer,QuestionPaperSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NotesSerializer(data=request.data)
    if serializer.is_valid():
        # Associate the logged-in user with the note
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question_paper(request):
    serializer = QuestionPaperSerializer(data=request.data)
    if serializer.is_valid():
        # Save the question paper if the data is valid
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_notes(request):
    notes = Notes.objects.all()
    serializer = NotesSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question_paper(request):
    question_paper = QuestionPaper.objects.all()
    serializer = QuestionPaperSerializer(question_paper, many=True)
    return Response(serializer.data)