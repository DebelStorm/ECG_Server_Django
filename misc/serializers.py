from rest_framework import serializers
from .models import user_device_mapping
from django.contrib.auth.models import User

class DeviceSerializerListing(serializers.ModelSerializer):
    class Meta:
        model = user_device_mapping
        fields = ['user_id_fk', 'device_id_fk']
        depth = 1
