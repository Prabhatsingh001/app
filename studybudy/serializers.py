from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField

CustomUser = get_user_model()
class SignupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=20)
    gender = serializers.CharField(max_length=10,)
    phone_number = PhoneNumberField(allow_null=True, allow_blank=True)
    date_of_birth = serializers.DateField()
    profile_picture = serializers.ImageField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password2 = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "gender",
            "phone_number",
            "date_of_birth",
            "profile_picture",
            "password",
            "password2",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id" : {"read_only": True},
            "profile_picture": {"required": False},
            "phone_number": {"required": False},
            "gender": {"required": False},
            "date_of_birth": {"required": False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required = True)
    password = serializers.CharField(required=True,write_only=True)


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


# FOR CHANGE PASSWORD
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            EmailValidator()(value)
            return value
        except ValidationError:
            raise serializers.ValidationError("use a valid email")
        
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
    confirm_password = serializers.CharField(write_only=True, required=True)