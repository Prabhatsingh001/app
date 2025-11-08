from rest_framework.response import Response
from .models import CustomUser
# from django.shortcuts import get_object_or_404
from studybudy.serializers import SignupSerializer,LoginSerializer,UpdateProfileSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"] #type: ignore
    password = serializer.validated_data['password'] #type: ignore
    user = authenticate(request=request, email=email, password=password)
    if user is None:
        user = CustomUser.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response({"success":False,"error": "Invalid_Credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    if not getattr(user, "is_active", True):
        return Response(
            {'success': False, 'error': 'Account disabled'},
            status=status.HTTP_403_FORBIDDEN
        )
    refresh = RefreshToken.for_user(user)
    return Response({
        "success": True,
        "message": "Login successful",
        "data": {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.pk,
                'username': user.username,
                'email': user.email
            }
        },
        'Required': 'Please update your profile to complete your account setup.'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user  = request.user
    profile_picture_url = user.profile_picture.url if user.profile_picture else None
    return Response({
        "id" : user.id,
        "profile_picture": profile_picture_url,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender" : user.gender,
        "phone_number" : user.phone_number,
        "date_of_birth" : user.date_of_birth
    }, status=status.HTTP_200_OK)


@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def Update_Profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    serializer = UpdateProfileSerializer(user, data=request.data, partial = True)
    if serializer.is_valid():
        serializer.save()            
        return Response({
            "message" : "Profile updated successfully",
            "user" : serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    user = request.user
    if user:
        user.delete()
        return Response({"message": "User profile deleted successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_picture(request):
    user = request.user
    if user.profile_picture:
        user.profile_picture.delete()
        return Response({"message": "Profile picture deleted successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "Profile picture not found."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST)
