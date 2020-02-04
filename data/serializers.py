from rest_framework import serializers
from .models import Data

class DataUploadSerializer(serializers.Serializer):
    device_sl_no = serializers.CharField(max_length = 100, required = True)
    patient_no = serializers.CharField(max_length = 100, required = True)
    File = serializers.FileField(required = True)
    Start_Time = serializers.TimeField()
    End_Time = serializers.TimeField()
