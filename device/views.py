from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Device
from .serializers import DeviceSerializer, DeleteSerializer, UpdateSerializer, AddDeviceSerializer, get_ota_serializer, get_session_id_serializer
from .permissions import IsSuperUserOrReadOnly
from misc.models import user_device_mapping
from firmware.models import Firmware_Version
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.exceptions import ParseError

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

class show_devices(APIView):
    def get(self, request):
        try:
            serializer = get_session_id_serializer(data = request.data)
        except:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):

            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                user_device_set = user_device_mapping.objects.filter(user_id_fk = current_user)

                json_objects = []

                for usr_device_object in user_device_set.iterator():

                    device_object = usr_device_object.device_id_fk
                    device_firmware_object = Firmware_Version.objects.get(device_id_fk = device_object)

                    return_data = {
                        'device_name' : device_object.device_name,
                        'serial_number' : device_object.serial_number,
                        'Mac_id' : device_object.Mac_id,
                        'Num_of_Leads' : device_object.Num_of_Leads,
                        'Firmware_Version_id' : device_firmware_object.Firmware_Version_id ,
                        'Firmware_version_number' : device_firmware_object.Firmware_version_number
                    }

                    json_objects += [return_data]

                return Response(data = json_objects, status = status.HTTP_200_OK)

            return Response({"error" : "INVALID SESSION", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

class get_ota(APIView):
    def get(self, request):
        try:
            serializer = get_ota_serializer(data = request.data)
        except:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):

            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)

                current_user = token_object.user
                serial_number = serializer.validated_data.get("serial_number")

                device_set = Device.objects.filter(serial_number = serial_number)

                if(device_set.exists()):

                    device_object = Device.objects.get(serial_number = serial_number)
                    device_firmware_object = Firmware_Version.objects.get(device_id_fk = device_object)

                    return_data = {
                        'device_name' : device_object.device_name,
                        'serial_number' : device_object.serial_number,
                        'Mac_id' : device_object.Mac_id,
                        'Num_of_Leads' : device_object.Num_of_Leads,
                        'Firmware_Version_id' : device_firmware_object.Firmware_Version_id ,
                        'Firmware_version_number' : device_firmware_object.Firmware_version_number
                    }

                    return Response(data = return_data, status = status.HTTP_200_OK)

                return Response({"error" : "DEVICE DOES NOT EXIST", "status" : "FAIL"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "INVALID SESSION", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

# Update Device API
@api_view(['POST'])
def update_device_settings(request):
    if(request.method == 'POST'):
        try:
            serializer = UpdateSerializer(data = request.data)
        except:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                set = Device.objects.filter(serial_number = serializer.validated_data.get('serial_number'))

                if(set.exists()):

                    device_to_be_updated = Device.objects.get(serial_number = serializer.validated_data.get('serial_number'))
                    set2 = user_device_mapping.objects.filter(user_id_fk = current_user, device_id_fk = device_to_be_updated)

                    if(set2.exists() or current_user.is_staff):

                        new_device_name = serializer.validated_data.get('device_name')
                        new_Firmware_Version_id = serializer.validated_data.get('Firmware_version_id')
                        new_Firmware_version_number = serializer.validated_data.get('Firmware_version_number')
                        new_Mac_id = serializer.validated_data.get('Mac_id')
                        new_Num_of_Leads  = serializer.validated_data.get('Num_of_Leads')

                        if(new_device_name != None):
                            device_to_be_updated.device_name = new_device_name
                        if(new_Mac_id != None):
                            device_to_be_updated.Mac_id = new_Mac_id
                        if(new_Num_of_Leads != None):
                            device_to_be_updated.Num_of_Leads = new_Num_of_Leads

                        device_firmware_object = Firmware_Version.objects.get(device_id_fk = device_to_be_updated)

                        if(new_Firmware_Version_id != None):
                            device_firmware_object.Firmware_Version_id = new_Firmware_Version_id
                        if(new_Firmware_version_number != None):
                            device_firmware_object.Firmware_version_number = new_Firmware_version_number

                        device_to_be_updated.save()
                        device_firmware_object.save()

                        return Response({"status" : "SUCCESS"},status=status.HTTP_200_OK)

                    return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

                return Response({"error" : "DEVICE DOES NOT EXIST", "status" : "FAIL"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "INVALID SESSION", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

## DELETE DEVICE API
@api_view(['POST'])
def delete_device(request):
    if(request.method == 'POST'):
        try:
            serializer = DeleteSerializer(data = request.data)
        except:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user
                set = Device.objects.filter(serial_number = serializer.validated_data.get('serial_number'))

                if(set.exists()):

                    device_to_be_deleted = Device.objects.get(serial_number = serializer.validated_data.get('serial_number'))
                    set2 = user_device_mapping.objects.filter(user_id_fk = current_user, device_id_fk = device_to_be_deleted)

                    if(set2.exists() or current_user.is_staff):

                        device_to_be_deleted.delete()
                        return Response({"status" : "SUCCESS"}, status=status.HTTP_200_OK)

                    return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

                return Response({"error" : "DEVICE DOES NOT EXIST", "status" : "FAIL"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "INVALID SESSION", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

##  ADD DEVICE API
@api_view(['POST'])
def add_device(request):
    if(request.method == 'POST'):
        try:
            serializer = AddDeviceSerializer(data = request.data)
        except:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):

            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                if(not Device.objects.filter(serial_number = serializer.validated_data.get('serial_number')).exists()):

                    device_name = serializer.validated_data.get("device_name")
                    if(device_name is None):
                        device_name = "DefaultDevice"
                    serial_number = serializer.validated_data.get("serial_number")
                    Mac_id = serializer.validated_data.get("Mac_id")
                    if(Mac_id is None):
                        Mac_id = "N/A"
                    Num_of_Leads = serializer.validated_data.get("Num_of_Leads")
                    if(Num_of_Leads is None):
                        Num_of_Leads = 12
                    new_device = Device(device_name = device_name, serial_number = serial_number, Mac_id = Mac_id, Num_of_Leads = Num_of_Leads)
                    new_device.save()
                    add_firmware = Firmware_Version(device_id_fk = new_device)
                    add_firmware.save()

                new_device = Device.objects.get(serial_number = serializer.validated_data.get('serial_number'))

                if(not user_device_mapping.objects.filter(user_id_fk = current_user, device_id_fk = new_device).exists()):

                    new_u_d_map = user_device_mapping(user_id_fk = current_user, device_id_fk = new_device)
                    new_u_d_map.save()

                return Response({"status" : "SUCCESS"}, status=status.HTTP_201_CREATED)

            return Response({"error" : "INVALID AUTH", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)
