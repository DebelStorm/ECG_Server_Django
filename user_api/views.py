from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserShowOnlySerializer, UserCreateSerializer, UserUpdateSerializer, ForgotPasswordSerializer, LoginSerializer, LogoutSerializer
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
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.

from django.contrib.auth.decorators import login_required

def test_redirect(request):
    return HttpResponseRedirect("api/login")

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data = request.data)
        if(serializer.is_valid()):
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(username = username, password = password)
            if user is not None:
                token_set = Token.objects.filter(user = user)
                if(token_set.exists()):
                    token = Token.objects.get(user = user)
                    token.delete()
                    new_token = Token.objects.create(user = user)
                    token = new_token
                else:
                    token = Token.objects.create(user = user)
                return Response(token.key, status = status.HTTP_200_OK)
            else:
                return Response("Login Failed. Check username/password.", status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data = request.data)
        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)
            if(token_set.exists()):
                token_object = Token.objects.get(key = session_id)
                token_object.delete()
                return Response("SUCCESS", status = status.HTTP_200_OK)
            else:
                return Response("Already Logged Out.", status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserShowOnlySerializer
    permission_classes = [IsSuperUserOnly]

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsSuperUserOnly]
    parser_classes = (JSONParser, MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if(serializer.is_valid()):
            Password = serializer.validated_data.get('password')
            Confirm_Password = serializer.validated_data.get('Confirm_Password')
            if(Confirm_Password == Password):
                #serializer.create(serializer.validated_data)
                phone_number = serializer.validated_data.get('phone_number')
                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')
                first_name = serializer.validated_data.get('first_name')
                last_name = serializer.validated_data.get('last_name')
                email = serializer.validated_data.get('email')
                user = User.objects.create_user(username = username, password = password, first_name = first_name, last_name = last_name, email = email)
                if(phone_number != None):
                    user.profile = Profile.objects.create(user = user, phone_number = phone_number)
                else:
                    user.profile = None
                user.save()
                return Response("SUCCESS", status = status.HTTP_200_OK)
            else:
                return Response("Check Password and Confirm Password", status = status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status = status.HTTP_406_NOT_ACCEPTABLE)

    def perform_create(self, serializer):
        try:
            if(serializer.is_valid()):
                serializer.save()
        except:
            pass

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
            return Response("FAIL", status=status.HTTP_401_UNAUTHORIZED)
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
                return Response("SUCCESS", status = status.HTTP_200_OK)
            return Response(serializer.errors)

class ForgotPassword(APIView):

    #serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = ForgotPasswordSerializer(data = request.data)

        if(serializer.is_valid()):
            email = serializer.validated_data.get('email')
            set = User.objects.filter(username = serializer.validated_data.get('username'))

            if(set.exists() and (len(set) == 1)):

                current_user = User.objects.get(username = serializer.validated_data.get('username'))
                user_mail = current_user.email

                if(user_mail == email):

                    OTP = serializer.validated_data.get('OTP')
                    OTP_req = current_user.profile.OTP

                    if(OTP == OTP_req):

                        new_pass1 = serializer.validated_data.get('new_password')
                        new_pass2 = serializer.validated_data.get('new_password_confirm')

                        if((new_pass1 == None) or (new_pass2 == None)):

                            return Response("Please enter both new_password and new_password_confirm.", status = status.HTTP_406_NOT_ACCEPTABLE)

                        elif(new_pass1 == new_pass2):

                            current_user.set_password(new_pass1)
                            current_user.save()

                            hotp = pyotp.HOTP(pyotp.random_base32())
                            key = hotp.at(100)
                            current_user.profile.OTP = key
                            current_user.profile.save()

                            return Response("Password Updated Successfully.", status = status.HTTP_200_OK)

                        else:

                            return Response("Password and Confirm Password not same", status = status.HTTP_200_OK)

                    elif(OTP == None):

                        hotp = pyotp.HOTP(pyotp.random_base32())
                        key = hotp.at(100)
                        current_user.profile.OTP = key
                        current_user.profile.save()
                        try:
                            send_mail("OTP", key, EMAIL_HOST_USER, [user_mail], fail_silently=False,)
                        except BadHeaderError:
                            return Response("Invalid header found.")
                        return Response("OTP Sent to registered mail.", status = status.HTTP_200_OK)

                    else:
                        return Response("INVALID OTP", status = status.HTTP_406_NOT_ACCEPTABLE)
                else:

                    return Response("Check username/email", status = status.HTTP_406_NOT_ACCEPTABLE)

            return Response("FAIL", status = status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status = status.HTTP_406_NOT_ACCEPTABLE)
