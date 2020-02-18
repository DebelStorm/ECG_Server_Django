from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User, AnonymousUser

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number']

class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs =  {
                            'username' : {'required' : True},
                            'password' : {'required' : True, 'write_only' : True, 'style' : {'input_type': 'password', 'placeholder': 'Password'}}
                        }

class LogoutSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)

class UserCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length = 20, required = False)
    Confirm_Password = serializers.CharField(write_only = True, required = True, style = {'input_type': 'password', 'placeholder': 'Password'})
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'Confirm_Password' , 'first_name', 'last_name', 'email', 'phone_number']
        extra_kwargs =  {
                            'password' : {'required' : True, 'write_only' : True, 'style' : {'input_type': 'password', 'placeholder': 'Password'}}
                        }

    #def create(self, validated_data):
    #    Profile_data = validated_data.pop('profile')
    #    username = validated_data.get('username')
    #    password = validated_data.get('password')
    #    first_name = validated_data.get('first_name')
    #    last_name = validated_data.get('last_name')
    #    email = validated_data.get('email')
    #    user = User.objects.create_user(username = username, password = password, first_name = first_name, last_name = last_name, email = email)
    #    user.profile = Profile.objects.create(user = user, **Profile_data)
    #    user.save()
    #    return user

class UserShowOnlySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    #user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']
        #extra_kwargs = {'profile' : {'required' : False}}

    def create(self, validated_data):
        Profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        user.profile = Profile.objects.create(user = user, **Profile_data)
        user.save()
        return user

class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 50, required = False)
    first_name = serializers.CharField(max_length = 50, required = False)
    last_name = serializers.CharField(max_length = 50, required = False)
    email = serializers.EmailField(max_length = 50, required = False)
    phone_number = serializers.CharField(max_length = 20, required = False)
    #OTP = serializers.CharField(max_length = 6, required = False)

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 50, required = True)
    email = serializers.EmailField(max_length = 50, required = True)
    OTP = serializers.CharField(max_length = 6, required = False)
    new_password = serializers.CharField(required = False)
    new_password_confirm = serializers.CharField(required = False)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 50, required = True)
    password = serializers.CharField(write_only = True, required = True, style = {'input_type': 'password', 'placeholder': 'Password'})
