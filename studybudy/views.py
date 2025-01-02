from rest_framework.response import Response
from .models import CustomUser
from studybudy.serializers import SignupSerializer,LoginSerializer,UpdateProfileSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError


# for signup
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # print({"message": "User registered successfully!"})
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


# for forgot password  or password reset request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CustomUser #assuming you have a user model
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import PasswordReset
from .serializers import ResetPasswordRequestSerializer,ResetPasswordSerializer
import os

class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        user = CustomUser.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}"

            # Sending reset link via email (commented out for clarity)
            # ... (email sending code)

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        new_password = data['new_password']
        confirm_password = data['confirm_password']
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        
        if not reset_obj:
            return Response({'error':'Invalid token'}, status=400)
        
        user = User.objects.filter(email=reset_obj.email).first()
        
        if user:
            user.set_password(request.data['new_password'])
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Password updated'})
        else: 
            return Response({'error':'No user found'}, status=404)