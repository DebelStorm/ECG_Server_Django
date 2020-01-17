from django.shortcuts import render
from .models import user_device_mapping
from rest_framework import permissions
from .serializers import DeviceSerializerListing
from .permissions import IsAuthenticatedAndUserOnly
from rest_framework import generics

# Create your views here.
class ShowAllUserDevices(generics.ListAPIView):
    queryset = user_device_mapping.objects.all()
    serializer_class = DeviceSerializerListing

class AddDeleteUserDevices(generics.RetrieveUpdateDestroyAPIView):
    queryset = user_device_mapping.objects.all()
    serializer_class = DeviceSerializerListing
    permissions = [IsAuthenticatedAndUserOnly]
