from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Device
from .serializers import DeviceSerializer
from .permissions import IsSuperUserOrReadOnly

# Create your views here.

class ShowAllDevices(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class AddDeleteDevice(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permissions = [permissions.IsAdminUser]
