from rest_framework.response import Response
from .models import CustomUser
from studybudy.serializers import SignupSerializer,LoginSerializer,UpdateProfileSerializer,PasswordResetRequestSerializer,PasswordResetConfirmSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse



# for signup
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print({"message": "User registered successfully!"})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# for login
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username_or_email = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        if '@' in username_or_email:
            try:
                user = CustomUser.objects.get(email=username_or_email)
            except CustomUser.DoesNotExist:
                return Response({'success': False, 'error': 'invalid emial or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = CustomUser.objects.get(username=username_or_email)
            except CustomUser.DoesNotExist:
                return Response({'success': False, 'error': 'invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Login successful",
                "data": {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                },
                'Required': 'Please update your profile to complete your account setup.'
            }, status=status.HTTP_200_OK)
        return Response({'success': False, 'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#for logout
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


#for user info in dashboard
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


#for user to update his/her profile
@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def Update_Profile(request):
    user = request.user
    serializer = UpdateProfileSerializer(user, data=request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message" : "Profile updated successfully",
            "user" : serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to delete user profile
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    user = request.user
    if user:
        user.delete()
        return Response({"message": "User profile deleted successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


#to generate new access token
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  # Optionally, require the user to be authenticated
# def refresh_access_token(request):
#     try:
#         refresh_token = request.data.get('refresh')
#         if not refresh_token:
#             return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
#         token = RefreshToken(refresh_token)
#         new_access_token = str(token.access_token)
#         return Response({
#             "access": new_access_token
#         }, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#to change password
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



#to request password reset
class PasswordResetRequestView(APIView):
    """
    Request a password reset by sending an email to the user.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"detail": "Email not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate reset token and uidb64
            uidb64 = urlsafe_base64_encode(str(user.pk).encode()).decode()
            token = default_token_generator.make_token(user)

            # Create reset URL
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            reset_link = f"{settings.FRONTEND_URL}{reset_url}"

            # Send password reset email
            subject = "Password Reset Request"
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#to reset password
class PasswordResetConfirmView(APIView):
    """
    Confirm the password reset using the token and uidb64 provided in the link.
    """
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, CustomUser.DoesNotExist):
            return Response({"detail": "Invalid or expired link."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the token
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired link."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the new password
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['password']

            try:
                password_validation.validate_password(new_password, user)
            except ValidationError as e:
                return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
