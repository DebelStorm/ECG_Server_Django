from rest_framework import serializers
from .models import Data

class DataUploadSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    overwrite = serializers.BooleanField(default = False)
    data_id = serializers.CharField(max_length = 50, required = True)
    device_sl_no = serializers.CharField(max_length = 100, required = True)
    patient_no = serializers.CharField(max_length = 100, required = True)
    File_location = serializers.CharField(max_length = 100,required = True)
    Start_Time = serializers.IntegerField(required = True)
    End_Time = serializers.IntegerField(required = True)

class BDFE_DataUploadSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    overwrite = serializers.BooleanField(default = False)
    data_id = serializers.CharField(max_length = 50, required = True)
    File_location = serializers.CharField(max_length = 100,required = True)

class DataDownloadSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    patient_no = serializers.CharField(max_length = 50, required = True)
    serial_number = serializers.CharField(max_length = 100, required=True)
    get_bdfe = serializers.BooleanField(default = False)
    Start_Time = serializers.IntegerField(required = True)
    End_Time = serializers.IntegerField()
    download_mode = serializers.IntegerField(default = 0)  # 0-> file, 1-> file+BDFE
    include_bdfe_index = serializers.IntegerField(default = 0) # 0->do not include index, 1->include index
    show_all_averages = serializers.IntegerField(default = 0)

#class DataDownloadSerializer(serializers.Serializer):
#    session_id = serializers.CharField(max_length = 100, required = True)
#    data_id = serializers.CharField(max_length = 50, required = True)
