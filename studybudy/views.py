"""StudyBuddy Authentication and Profile Management Views.

This module provides API views for user authentication (signup, login, logout),
profile management (update, delete), and account operations (change password,
manage profile picture). All views return JSON responses and use JWT for auth.

Authentication:
    - Most endpoints require JWT authentication via Authorization header
    - Login and signup endpoints are publicly accessible
    - Token refresh endpoint requires a valid refresh token

Available endpoints:
    POST /signup/ - Create new user account
    POST /login/ - Authenticate and get JWT tokens
    POST /logout/ - Blacklist refresh token
    GET /dashboard/ - Get user profile data
    PUT/PATCH /update_profile/ - Update user profile
    DELETE /delete_profile/ - Delete user account
    POST /change_password/ - Update password
    DELETE /delete_profile_picture/ - Remove profile picture
"""

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from studybudy.serializers import (
    LoginSerializer,
    SignupSerializer,
    UpdateProfileSerializer,
)

from .models import CustomUser


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    """Create a new user account.

    Args:
        request: HTTP request object with user data in request.data
                Expected fields defined in SignupSerializer

    Returns:
        Response: JSON containing user data on success
        Status codes:
            201: User created successfully
            400: Invalid data provided

    Example request:
        POST /signup/
        {
            "email": "user@example.com",
            "username": "username",
            "password": "secure_password"
        }
    """
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Authenticate user and return JWT tokens.

    Args:
        request: HTTP request object containing login credentials
                Required fields: email, password

    Returns:
        Response: JSON with tokens and user data on success
        Status codes:
            200: Login successful
            401: Invalid credentials
            403: Account disabled

    Example request:
        POST /login/
        {
            "email": "user@example.com",
            "password": "user_password"
        }

    Success response includes:
        - refresh token
        - access token
        - user details (id, username, email)
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]  # type: ignore
    password = serializer.validated_data["password"]  # type: ignore
    user = authenticate(request=request, email=email, password=password)
    if user is None:
        user = CustomUser.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response(
                {"success": False, "error": "Invalid_Credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    if not getattr(user, "is_active", True):
        return Response(
            {"success": False, "error": "Account disabled"},
            status=status.HTTP_403_FORBIDDEN,
        )
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "success": True,
            "message": "Login successful",
            "data": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {"id": user.pk, "username": user.username, "email": user.email},
            },
            "Required": "Please update your profile to complete your account setup.",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def get_access_token(request):
    """Generate new access token using refresh token.

    Args:
        request: HTTP request object with refresh token in request.data
                Required field: refresh

    Returns:
        Response: JSON with new access token
        Status codes:
            200: New access token generated
            400: Missing refresh token
            401: Invalid/expired refresh token

    Example request:
        POST /token/refresh/
        {
            "refresh": "your-refresh-token"
        }
    """
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"error": "Refresh Token is Required"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)
        new_access = str(token.access_token)
        return Response({"access_token": new_access}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {"error": "Invalid or expired Refresh Token please Login again"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "User logged out successfully."}, status=status.HTTP_200_OK
        )

    except TokenError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": "An unexpected error occurred: " + str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    """Retrieve user's profile data.

    Args:
        request: HTTP request object (must be authenticated)

    Returns:
        Response: JSON containing user profile data
        Status codes:
            200: Profile data retrieved successfully

    Response includes:
        - Basic info (id, username, email)
        - Profile picture URL (if exists)
        - Personal info (name, gender, phone, DOB)
    """
    user = request.user
    profile_picture_url = user.profile_picture.url if user.profile_picture else None
    return Response(
        {
            "id": user.id,
            "profile_picture": profile_picture_url,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender,
            "phone_number": user.phone_number,
            "date_of_birth": user.date_of_birth,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def Update_Profile(request):
    """Update user profile information.

    Supports both PUT (full update) and PATCH (partial update).
    Uses UpdateProfileSerializer for validation.

    Args:
        request: HTTP request with profile data to update
                Fields defined in UpdateProfileSerializer

    Returns:
        Response: JSON with success message and updated user data
        Status codes:
            200: Profile updated successfully
            400: Invalid data provided
    """
    user = request.user
    serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Profile updated successfully", "user": serializer.data},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    """Delete user account permanently.

    Args:
        request: HTTP request (must be authenticated)

    Returns:
        Response: JSON with success/error message
        Status codes:
            200: Profile deleted successfully
            404: User not found
    """
    user = request.user
    if user:
        user.delete()
        return Response(
            {"message": "User profile deleted successfully."}, status=status.HTTP_200_OK
        )
    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_profile_picture(request):
    """Delete user's profile picture.

    Args:
        request: HTTP request (must be authenticated)

    Returns:
        Response: JSON with success/error message
        Status codes:
            200: Picture deleted successfully
            404: No profile picture found
    """
    user = request.user
    if user.profile_picture:
        user.profile_picture.delete()
        return Response(
            {"message": "Profile picture deleted successfully."},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"error": "Profile picture not found."}, status=status.HTTP_404_NOT_FOUND
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user's password.

    Requires current password verification before allowing change.

    Args:
        request: HTTP request with password data
                Required fields:
                - old_password: Current password
                - new_password: New password to set

    Returns:
        Response: JSON with success/error message
        Status codes:
            200: Password changed successfully
            400: Invalid old password

    Example request:
        POST /change_password/
        {
            "old_password": "current_password",
            "new_password": "new_secure_password"
        }
    """
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Password changed successfully."}, status=status.HTTP_200_OK
        )
    return Response(
        {"error": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST
    )
