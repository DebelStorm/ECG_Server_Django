from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, UserShowOnlySerializer
from rest_framework import generics, permissions, status
from user_api.permissions import IsOwnerOrSuperUser, IsSuperUserOnly
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Profile
# Create your views here.

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserShowOnlySerializer
    permission_classes = [IsSuperUserOnly]

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserShowOnlySerializer
    permission_classes = [IsSuperUserOnly]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserShowOnlySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperUser]
