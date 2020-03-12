from django.shortcuts import render
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view
from .forms import DataUploadForm
from .serializers import DataUploadSerializer, DataDownloadSerializer, DataUploadSerializerJSON
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
import csv
from os import path
import io

# Create your views here.

'''
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
                        Start_Time = serializer.validated_data.get('Start_Time')
                        End_Time = serializer.validated_data.get('End_Time')
                        File = serializer.validated_data.get('File')

                        if(Start_Time >= End_Time):
                            return Response({"error" : "Start_Time must be less than End_Time.", "status" : "FAIL"}, status=status.HTTP_400_BAD_REQUEST)

                        overwrite = serializer.validated_data.get('overwrite')

                        if(not Data.objects.filter(data_file_id = data_id).exists()):

                            new_file = Data(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = File, Start_Time = Start_Time, End_Time = End_Time)
                            new_file.save()

                            #

                            #

                            return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                        elif(overwrite):

                            old_file = Data.objects.get(data_file_id = data_id)

                            old_file_user = old_file.user_id_fk

                            if(old_file_user == current_user):

                                old_file.delete()

                                new_file = Data(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = File, Start_Time = Start_Time, End_Time = End_Time)
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
'''

class post_data_JSON(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = DataUploadSerializerJSON(data = request.data)
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
                        Start_Time = serializer.validated_data.get('Start_Time')
                        End_Time = serializer.validated_data.get('End_Time')
                        File = serializer.validated_data.get('File_location')

                        if(not path.exists(File)):
                            return Response({"error" : "File does not exist in server.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)

                        if(Start_Time >= End_Time):
                            return Response({"error" : "Start_Time must be less than End_Time.", "status" : "FAIL"}, status=status.HTTP_400_BAD_REQUEST)

                        overwrite = serializer.validated_data.get('overwrite')

                        if(not Data.objects.filter(data_file_id = data_id).exists()):

                            new_file = Data(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = File, Start_Time = Start_Time, End_Time = End_Time)
                            new_file.save()
                            return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                        elif(overwrite):

                            old_file = Data.objects.get(data_file_id = data_id)

                            old_file_user = old_file.user_id_fk

                            if(old_file_user == current_user):

                                old_file.delete()

                                new_file = Data(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = File, Start_Time = Start_Time, End_Time = End_Time)
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

class post_proccessed_data_JSON(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = DataUploadSerializerJSON(data = request.data)
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
                        Start_Time = serializer.validated_data.get('Start_Time')
                        End_Time = serializer.validated_data.get('End_Time')
                        File = serializer.validated_data.get('File_location')

                        if(not path.exists(File)):
                            return Response({"error" : "File does not exist in server.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)

                        if(Start_Time >= End_Time):
                            return Response({"error" : "Start_Time must be less than End_Time.", "status" : "FAIL"}, status=status.HTTP_400_BAD_REQUEST)

                        overwrite = serializer.validated_data.get('overwrite')

                        if(not Data_filtered.objects.filter(data_file_id = data_id).exists()):

                            new_file = Data_filtered(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = File, Start_Time = Start_Time, End_Time = End_Time)
                            new_file.save()
                            return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                        elif(overwrite):

                            old_file = Data_filtered.objects.get(data_file_id = data_id)

                            old_file_user = old_file.user_id_fk

                            if(old_file_user == current_user):

                                old_file.delete()

                                new_file = Data_filtered(data_file_id = data_id , device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = File, Start_Time = Start_Time, End_Time = End_Time)
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

'''
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
'''

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

class get_data_via_times(APIView):
    def post(self, request):
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

                patient_no = serializer.validated_data.get("patient_no")
                Start_Time = serializer.validated_data.get("Start_Time")
                End_Time = serializer.validated_data.get("End_Time")

                if End_Time is not None and Start_Time >= End_Time:
                    return Response({"error" : "Start_Time must be less than End_Time.", "status" : "FAIL"}, status=status.HTTP_400_BAD_REQUEST)

                serial_number = serializer.validated_data.get("serial_number")

                patient_set = Patient.objects.filter(patient_number = patient_no)
                device_set = Device.objects.filter(serial_number = serial_number)

                if(patient_set.exists()):
                    if(device_set.exists()):

                        patient_obj = Patient.objects.get(patient_number = patient_no)
                        device_obj = Device.objects.get(serial_number = serial_number)

                        data_files_objects = Data_filtered.objects.filter(device_id_fk = device_obj, patient_id_fk = patient_obj).order_by('Start_Time')
                        
                        if(End_Time is None):
                            data_files_objects = data_files_objects.filter(End_Time__gt = Start_Time)
                        else:
                            data_files_objects = data_files_objects.filter(End_Time__gt = Start_Time, Start_Time__lt = End_Time)

                        if(data_files_objects.exists()):

                            Start_Time_set = []
                            End_Time_set = []
                            Data_start_indexes = []
                            file_Data = []
                            no_of_rows = []

                            for data_file_object in data_files_objects:

                                Current_File_path = data_file_object.File
                                Current_File = io.open(Current_File_path, encoding = 'utf8')
                                content = str(Current_File.read()).split("\n")
                                #content = csv.reader(content, delimiter = ",")
                                #content = [x for x in content if x != []]
                                content = [x for x in content if x != ""]
                                Current_File.close()
                                file_Data += [content]
                                no_of_rows += [len(content)]
                                Start_Time_of_Current_File = data_file_object.Start_Time
                                End_Time_of_Current_File = data_file_object.End_Time

                                Start_Time_set += [Start_Time_of_Current_File]
                                End_Time_set += [End_Time_of_Current_File]

                            response = {
                                'status' : 'SUCCESS',
                                'no_of_files' : len(file_Data),
                                'Start_Time_set' : Start_Time_set,
                                'End_Time_set' : End_Time_set,
                                'No_of_records' : no_of_rows,
                                'Data' : file_Data
                            }

                            return Response(response, status = status.HTTP_200_OK)

                        return Response({"error" : "NO RECORDS FOUND FOR THE GIVEN TIME PERIOD.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
                    return Response({"error" : "DEVICE DETAILS NOT FOUND.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
                return Response({"error" : "PATIENT DETAILS NOT FOUND.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)
