from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Notes
from .serializers import NotesSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NotesSerializer(data=request.data)
    if serializer.is_valid():
        # Save the note if the data is valid
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
