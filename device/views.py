from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Device
from .serializers import DeviceSerializer, DeleteSerializer, UpdateSerializer
from .permissions import IsSuperUserOrReadOnly
from misc.models import user_device_mapping
from firmware.models import Firmware_Version
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

# SHOW ALL DEVICES API
class ShowAllDevices(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

class DetailDevice(generics.RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsSuperUserOrReadOnly]

# Working on this

@api_view(['POST'])
def update_device_settings(request):
    if(not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        if(request.method == 'POST'):
            serializer = UpdateSerializer(data = request.data)
            if(serializer.is_valid()):
                set = Device.objects.filter(serial_number = serializer.validated_data.get('serial_number'))
                if(set.exists() and (len(set) == 1)):
                    device_to_be_updated = Device.objects.get(serial_number = serializer.validated_data.get('serial_number'))

                    new_device_name = serializer.validated_data.get('device_name')
                    new_Firmware_Version_id = serializer.validated_data.get('Firmware_Version_id')
                    new_Firmware_version_number = serializer.validated_data.get('Firmware_version_number')
                    new_Mac_id = serializer.validated_data.get('Mac_id')
                    new_Num_of_Leads  = serializer.validated_data.get('Num_of_Leads')

                    if(new_device_name != "NA"):
                        device_to_be_updated.device_name = new_device_name
                    if(new_Mac_id != "NA"):
                        device_to_be_updated.Mac_id = new_Mac_id
                    if(new_Num_of_Leads != -1):
                        device_to_be_updated.Num_of_Leads = new_Num_of_Leads

                    device_firmware_object = Firmware_Version.objects.get(device_id_fk = device_to_be_updated)

                    if(new_Firmware_Version_id != "NA"):
                        device_firmware_object.Firmware_Version_id = new_Firmware_Version_id
                    if(new_Firmware_version_number != "NA"):
                        device_firmware_object.Firmware_version_number = new_Firmware_version_number

                    device_to_be_updated.save()
                    device_firmware_object.save()

                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_409_CONFLICT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

## DELETE DEVICE API
@api_view(['POST'])
def delete_device(request):
    if(not request.user.is_authenticated or not request.user.is_staff):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        if(request.method == 'POST'):
            serializer = DeleteSerializer(data = request.data)
            if(serializer.is_valid()):
                set = Device.objects.filter(serial_number = serializer.validated_data.get('serial_number'))
                if(set.exists() and (len(set) == 1)):
                    device_to_be_deleted = Device.objects.get(serial_number = serializer.validated_data.get('serial_number'))
                    device_to_be_deleted.delete()
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_409_CONFLICT)
            return Response(status=status.HTTP_400_BAD_REQUEST)


##  ADD DEVICE API
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
                    add_firmware = Firmware_Version(device_id_fk = new_device)
                    add_firmware.save()

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
