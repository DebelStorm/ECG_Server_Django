from rest_framework import serializers
from .models import Device
from django.contrib.auth.models import User

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_name', 'serial_number', 'Mac_id', 'Num_of_Leads']

class DeleteSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length = 100, required=True)

class UpdateSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length = 100, required = True)
    device_name = serializers.CharField(max_length = 100, required = False)
    Firmware_Version_id = serializers.CharField(max_length = 100, required = False)
    Firmware_version_number = serializers.CharField(max_length = 100, required = False)
    Mac_id = serializers.CharField(max_length = 100, required = False)
    Num_of_Leads = serializers.IntegerField(required = False)
