from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number']

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
