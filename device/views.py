from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Device
from .serializers import DeviceSerializer
from .permissions import IsSuperUserOrReadOnly
from misc.models import user_device_mapping
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ShowAllDevices(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permissions = [permissions.IsAuthenticated]

class AddDeleteDevice(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permissions = [permissions.IsAuthenticated, permissions.IsAdminUser, IsSuperUserOrReadOnly]

@api_view(['POST'])
def add_device(request):
    if(not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        if(request.method == 'POST'):
            serializer = DeviceSerializer(data = request.data)
            if(serializer.is_valid()):

                # Check if the Device already exists or not
                if(not Device.objects.filter(device_name = serializer.validated_data.get('device_name')).exists()):
                    new_device = serializer.save()

                new_device = Device.objects.get(device_name = serializer.validated_data.get('device_name'))
                #new_device_id = new_device.id
                current_user = User.objects.get(username = request.user.get_username())
                #current_user_id = current_user.id
                new_u_d_map = user_device_mapping(user_id_fk = current_user, device_id_fk = new_device)

                # Check if already exists
                if(not user_device_mapping.objects.filter(user_id_fk = current_user, device_id_fk = new_device).exists()):
                    new_u_d_map.save()

                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
