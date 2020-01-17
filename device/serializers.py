from rest_framework import serializers
from .models import Device
from django.contrib.auth.models import User

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_name', 'serial_number', 'Mac_id', 'Num_of_Leads']
