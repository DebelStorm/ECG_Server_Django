from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserShowOnlySerializer, UserUpdateSerializer, ForgotPasswordSerializer
from rest_framework import generics, permissions, status
from user_api.permissions import IsOwnerOrSuperUser, IsSuperUserOnly
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.core.mail import send_mail, BadHeaderError
from Project.settings import EMAIL_HOST_USER, SECRET_KEY
from django.http import HttpResponseRedirect
import pyotp, random, base32_lib
# Create your views here.

from django.contrib.auth.decorators import login_required

def test_redirect(request):
    return HttpResponseRedirect("api/login")

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserShowOnlySerializer
    permission_classes = [IsSuperUserOnly]

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserShowOnlySerializer
    permission_classes = [IsSuperUserOnly]

'''
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    #lookup_field = "username"
    serializer_class = UserShowOnlySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperUser]
'''

class UserDetailView(APIView):
    parser_classes = (JSONParser,)

    def get(self, request):
        if(not request.user.is_authenticated):
            return Response("FAIL", status=status.HTTP_401_UNAUTHORIZED)#status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = UserShowOnlySerializer(request.user)
            return Response(serializer.data)

    def patch(self, request):
        if(not request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = UserUpdateSerializer(data = request.data)
            if(serializer.is_valid()):
                current_user = request.user
                profile = current_user.profile
                new_user_name = serializer.validated_data.get('username')
                new_first_name = serializer.validated_data.get('first_name')
                new_last_name = serializer.validated_data.get('last_name')
                new_email = serializer.validated_data.get('email')
                new_PHNO = serializer.validated_data.get('phone_number')
                #new_OTP = serializer.validated_data.get('OTP')

                if(new_user_name != None):
                    current_user.username = new_user_name
                if(new_first_name != None):
                    current_user.first_name = new_first_name
                if(new_last_name != None):
                    current_user.last_name = new_last_name
                if(new_email != None):
                    current_user.email = new_email
                if(new_PHNO != None):
                    current_user.profile.phone_number = new_PHNO

                current_user.save()
                current_user.profile.save()
                return Response(current_user)
            return Response(serializer.errors)

class ForgotPassword(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data = request.data)
        if(serializer.is_valid()):
            email = serializer.validated_data.get('email')
            set = User.objects.filter(username = serializer.validated_data.get('username'))
            if(set.exists() and (len(set) == 1)):
                current_user = User.objects.get(username = serializer.validated_data.get('username'))
                user_mail = current_user.email
                if(user_mail == email):
                    hotp = pyotp.HOTP(base32_lib.generate())
                    key = hotp.at(random.randint(1,1000))
                    current_user.profile.OTP = key
                    current_user.profile.save()
                    try:
                        send_mail("OTP", key, EMAIL_HOST_USER, [user_mail], fail_silently=False,)
                    except BadHeaderError:
                        return Response("Invalid header found.")
                    return Response("SUCCESS", status = status.HTTP_200_OK)
                return Response("Check username/email", status = status.HTTP_406_NOT_ACCEPTABLE)
            return Response("FAIL", status = status.HTTP_404_NOT_FOUND)
        return Response("FAIL", status = status.HTTP_406_NOT_ACCEPTABLE)
