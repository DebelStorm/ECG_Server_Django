from django.shortcuts import render
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view
from .forms import DataUploadForm
from .serializers import DataUploadSerializer, DataDownloadSerializer
from rest_framework.views import APIView
from device.models import Device
from patient.models import Patient
from .models import Data
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

# Create your views here.

class post_data_forms(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, *args, **kwargs):
        serializer = DataUploadSerializer(data = request.data)

        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                if(Device.objects.filter(serial_number = serializer.validated_data.get('device_sl_no')).exists() and Patient.objects.filter(patient_number = serializer.validated_data.get('patient_no')).exists()):

                    current_device = Device.objects.get(serial_number = serializer.validated_data.get('device_sl_no'))
                    current_patient = Patient.objects.get(patient_number = serializer.validated_data.get('patient_no'))

                    data_id = serializer.validated_data.get('data_id')

                    overwrite = serializer.validated_data.get('overwrite')

                    if(not Data.objects.filter(data_file_id = data_id).exists()):

                        new_file = Data(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = serializer.validated_data.get('File'), Start_Time = serializer.validated_data.get('Start_Time'), End_Time = serializer.validated_data.get('End_Time'))
                        new_file.save()

                        return Response("SUCCESS", status = status.HTTP_200_OK)

                    elif(overwrite):

                        old_file = Data.objects.get(data_file_id = data_id)

                        old_file_user = old_file.user_id_fk

                        if(old_file_user == current_user):

                            old_file.delete()

                            new_file = Data(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = serializer.validated_data.get('File'), Start_Time = serializer.validated_data.get('Start_Time'), End_Time = serializer.validated_data.get('End_Time'))
                            new_file.save()

                            return Response("SUCCESS (file Overwritten)", status = status.HTTP_200_OK)

                        return Response("CANNOT OVERWRITE FILE UPLOADED BY ANOTHER USER", status = status.HTTP_400_BAD_REQUEST)

                    return Response("FILE ALREADY EXISTS", status = status.HTTP_400_BAD_REQUEST)

                return Response("DEVICE/PATIENT INFO INVALID", status = status.HTTP_400_BAD_REQUEST)

            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class get_data_via_browser(APIView):
    def get(self, request, data_id):
        if(not request.user.is_authenticated):
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
        if(not Data.objects.filter(data_file_id = data_id).exists()):
            return Response("DOES NOT EXIST", status = status.HTTP_400_BAD_REQUEST)
        current_user = request.user
        file_to_be_sent = Data.objects.get(data_file_id = data_id)
        if(not (request.user == file_to_be_sent.user_id_fk)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        response = HttpResponse(file_to_be_sent.File, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=data.bin'
        return response


class get_data(APIView):
    def get(self, request):
        serializer = DataDownloadSerializer(data = request.data)
        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                data_id = serializer.validated_data.get("data_id")

                if(Data.objects.filter(data_file_id = data_id).exists()):

                    file_to_be_sent = Data.objects.get(data_file_id = data_id)

                    if(current_user == file_to_be_sent.user_id_fk):

                        response = HttpResponse(file_to_be_sent.File, content_type='text/plain')
                        response['Content-Disposition'] = 'attachment; filename=data.bin'

                        return response

                    return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

                return Response("FILE DOES NOT EXIST", status = status.HTTP_400_BAD_REQUEST)

            return Response("INVALID TOKEN", status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
