from rest_framework import serializers
from .models import Data

class DataUploadSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    overwrite = serializers.BooleanField(default = False)
    data_id = serializers.CharField(max_length = 50, required = True)
    device_sl_no = serializers.CharField(max_length = 100, required = True)
    patient_no = serializers.CharField(max_length =100, required = True)
    File = serializers.FileField(required = True)
    Start_Time = serializers.IntegerField(required = True)
    End_Time = serializers.IntegerField(required = True)

class DataUploadSerializerJSON(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    overwrite = serializers.BooleanField(default = False)
    data_id = serializers.CharField(max_length = 50, required = True)
    device_sl_no = serializers.CharField(max_length = 100, required = True)
    patient_no = serializers.CharField(max_length = 100, required = True)
    File_location = serializers.CharField(max_length = 100,required = True)
    Start_Time = serializers.IntegerField(required = True)
    End_Time = serializers.IntegerField(required = True)

class DataDownloadSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    patient_no = serializers.CharField(max_length = 50, required = True)
    serial_number = serializers.CharField(max_length = 100, required=True)
    Start_Time = serializers.IntegerField(required = True)
    End_Time = serializers.IntegerField()

#class DataDownloadSerializer(serializers.Serializer):
#    session_id = serializers.CharField(max_length = 100, required = True)
#    data_id = serializers.CharField(max_length = 50, required = True)
