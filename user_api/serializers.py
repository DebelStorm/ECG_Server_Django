from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'OTP']

class UserShowOnlySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']
        #extra_kwargs = {'password' : {'write_only' : True, 'required' : True}}

    def create(self, validated_data):
        Profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        user.profile = Profile.objects.create(user = user, **Profile_data)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'profile']
        #extra_kwargs = {'password' : {'write_only' : True, 'required' : True}}

    def create(self, validated_data):
        Profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        user.profile = Profile.objects.create(user = user, **Profile_data)
        user.save()
        return user
