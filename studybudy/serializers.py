from rest_framework import serializers
from .models import person,CustomUser

class peopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = person
        fields = '__all__'


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
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required=True,write_only=True)



#for updating profile
class UpdateProfileSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth']
        extra_kwargs = {
            'username':{'read_only':True},
            'email':{'read_only':True}
        }
