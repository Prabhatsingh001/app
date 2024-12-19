from rest_framework import serializers
from .models import CustomUser
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


# FOR SIGN UP
class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True) # Add password2 field for confirmation

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','password2','first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 since it's not needed for user creation
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    

# FOR LOGIN
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required=True,write_only=True)

    def validate_username(self,value):
        """
        Custom validation to handle both email and username.
        If the input is an email, it will return the email.
        If the input is a username, it will return the username.
        """
        if '@' in value:  # Check if it's an email
            try:
                EmailValidator()(value)
                return value
            except ValidationError:
                raise serializers.ValidationError("use a valid email or use a username")
        return value


#for updating profile
class UpdateProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_picture','phone_number', 'gender', 'date_of_birth']
        extra_kwargs = {
            'username':{'read_only':True},
            'email':{'read_only':True}
        }
