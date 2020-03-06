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
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

# Create your views here.

class post_data_forms(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, *args, **kwargs):
        try:
            serializer = DataUploadSerializer(data = request.data)
        except ParseError:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                if(Device.objects.filter(serial_number = serializer.validated_data.get('device_sl_no')).exists()):

                    if(Patient.objects.filter(patient_number = serializer.validated_data.get('patient_no')).exists()):

                        current_device = Device.objects.get(serial_number = serializer.validated_data.get('device_sl_no'))
                        current_patient = Patient.objects.get(patient_number = serializer.validated_data.get('patient_no'))

                        data_id = serializer.validated_data.get('data_id')

                        overwrite = serializer.validated_data.get('overwrite')

                        if(not Data.objects.filter(data_file_id = data_id).exists()):

                            new_file = Data(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = serializer.validated_data.get('File'), Start_Time = serializer.validated_data.get('Start_Time'), End_Time = serializer.validated_data.get('End_Time'))
                            new_file.save()

                            return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                        elif(overwrite):

                            old_file = Data.objects.get(data_file_id = data_id)

                            old_file_user = old_file.user_id_fk

                            if(old_file_user == current_user):

                                old_file.delete()

                                new_file = Data(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = serializer.validated_data.get('File'), Start_Time = serializer.validated_data.get('Start_Time'), End_Time = serializer.validated_data.get('End_Time'))
                                new_file.save()

                                return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                            return Response({"error" : "CANNOT OVERWRITE FILE UPLOADED BY ANOTHER USER", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

                        return Response({"error" : "FILE ALREADY EXISTS", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

                    return Response({"error" : "PATIENT INFO INVALID", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

                return Response({"error" : "DEVICE INFO INVALID", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)


class get_data_via_browser(APIView):
    def get(self, request, data_id):
        if(not request.user.is_authenticated):
            return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)
        if(not Data.objects.filter(data_file_id = data_id).exists()):
            return Response({"error" : "DOES NOT EXIST", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)
        current_user = request.user
        file_to_be_sent = Data.objects.get(data_file_id = data_id)
        if(not (request.user == file_to_be_sent.user_id_fk)):
            return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)
        response = HttpResponse(file_to_be_sent.File, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=data.bin'
        return response


class get_data(APIView):
    def get(self, request):
        try:
            serializer = DataDownloadSerializer(data = request.data)
        except ParseError:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

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

                        if(file_to_be_sent.File.storage.exists(file_to_be_sent.File.name)):

                            response = HttpResponse(file_to_be_sent.File, content_type='text/plain')
                            response['Content-Disposition'] = 'attachment; filename=data.bin'

                            return response

                        return Response({"error" : "FILE MISSING IN SERVER", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)

                    return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

                return Response({"error" : "FILE DOES NOT EXIST", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)
