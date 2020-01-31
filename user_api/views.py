from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, UserShowOnlySerializer
from rest_framework import generics, permissions, status
from user_api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Profile
# Create your views here.

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserShowOnlySerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
