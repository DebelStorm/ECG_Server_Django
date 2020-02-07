from django.shortcuts import render
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view
from .forms import DataUploadForm
from .serializers import DataUploadSerializer
from rest_framework.views import APIView
from device.models import Device
from patient.models import Patient
from .models import Data
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse

# Create your views here.

class post_data_forms(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, *args, **kwargs):
        if(not request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = DataUploadSerializer(data = request.data)
        #file = request.data['file']
        if(not serializer.is_valid()):
            return Response(serializer.errors)
        current_user = request.user
        if(Device.objects.filter(serial_number = serializer.validated_data.get('device_sl_no')).exists() and Patient.objects.filter(patient_number = serializer.validated_data.get('patient_no')).exists()):
            current_device = Device.objects.get(serial_number = serializer.validated_data.get('device_sl_no'))
            current_patient = Patient.objects.get(patient_number = serializer.validated_data.get('patient_no'))

            new_file = Data(data_file_id = serializer.validated_data.get('data_id'), device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = serializer.validated_data.get('File'), Start_Time = serializer.validated_data.get('Start_Time'), End_Time = serializer.validated_data.get('End_Time'))
            new_file.save()

            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class get_data(APIView):
    def get(self, request, fileid):
        if(not request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if(not Data.objects.filter(data_file_id = fileid).exists()):
            return Response(status = status.HTTP_400_BAD_REQUEST)
        current_user = request.user
        file_to_be_sent = Data.objects.get(data_file_id = fileid)
        if(not (request.user == file_to_be_sent.user_id_fk)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        response = HttpResponse(file_to_be_sent.File, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=data.bin'
        return response
