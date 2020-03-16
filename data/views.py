from django.shortcuts import render
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view
from .forms import DataUploadForm
from .serializers import DataUploadSerializer, DataDownloadSerializer, DataUploadSerializerJSON
from rest_framework.views import APIView
from device.models import Device
from patient.models import Patient
from .models import Data, Data_filtered
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import csv
from os import path
import io
import numpy as np

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

                            Current_starttime = 0
                            Current_endtime = 0
                            server_unavailability_flag = 0
                            time_unavailability_flag = 0
                            count = 0

                            for data_file_object in data_files_objects:

                                Current_File_path = data_file_object.File

                                if(not path.exists(Current_File_path)):
                                    server_unavailability_flag = 1
                                else:
                                    Current_File = io.open(Current_File_path, encoding = 'utf8')

                                    content = str(Current_File.read()).split("\n")
                                    content = csv.reader(content, delimiter = ",")
                                    content = [x for x in content if x != []]

                                    no_of_rows_current_file = len(content)
                                    content = np.asarray(content).T.tolist()

                                    #content = [x for x in content if x != ""]
                                    Current_File.close()
                                    file_Data += [content]
                                    no_of_rows += [no_of_rows_current_file]
                                    Start_Time_of_Current_File = data_file_object.Start_Time
                                    End_Time_of_Current_File = data_file_object.End_Time

                                    Start_Time_set += [Start_Time_of_Current_File]
                                    End_Time_set += [End_Time_of_Current_File]
                                    if(not count):
                                        Current_starttime = Start_Time_of_Current_File
                                        if Current_starttime != Start_Time:
                                            time_unavailability_flag = 1
                                        Current_endtime = End_Time_of_Current_File
                                        count += 1
                                    elif(count == 1):
                                        if(Start_Time_of_Current_File != Current_endtime):
                                            time_unavailability_flag = 1
                                            count += 1
                                        Current_endtime = End_Time_of_Current_File
                                        Current_starttime = Start_Time_of_Current_File

                            if Current_endtime != End_Time:
                                time_unavailability_flag = 1

                            no_of_files_var = len(file_Data)

                            final_data = []

                            for i in range(12):
                                con_array = []
                                for file in file_Data:
                                    con_array += file[i]

                                final_data += [con_array]              # Array Format
                                #final_data += [','.join(con_array)]     # Text Format

                            # Slicing of last and first file

                            frequency = 1000

                            if(no_of_files_var > 0):

                                start_time_slice = round((Start_Time - Start_Time_set[0]) * frequency)
                                end_time_slice = round((End_Time_set[-1] - End_Time) * frequency)

                                if(start_time_slice > 0):
                                    for i in range(len(final_data)):
                                        final_data[i] = final_data[i][start_time_slice : ]
                                    Start_Time_set[0] = Start_Time
                                    no_of_rows[0] -= start_time_slice

                                if(end_time_slice > 0):
                                    for i in range(len(final_data)):
                                        final_data[i] = final_data[i][ : -(end_time_slice)]
                                    End_Time_set[-1] = End_Time
                                    no_of_rows[-1] -= end_time_slice

                            response = {
                                'status' : 'SUCCESS',
                                'no_of_files' : no_of_files_var,
                                'Start_Time_set' : Start_Time_set,
                                'End_Time_set' : End_Time_set,
                                'No_of_records' : no_of_rows,
                                'Data' : final_data,
                            }

                            if(server_unavailability_flag):
                                response['message'] = 'Only partial data available. Some files missing in server.'
                            elif(time_unavailability_flag):
                                response['message'] = 'Only partial data available. Files not available for some time periods.'
                            else:
                                response['message'] = 'All data available.'
                            return Response(response, status = status.HTTP_200_OK)

                        return Response({"error" : "NO RECORDS FOUND FOR THE GIVEN TIME PERIOD.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
                    return Response({"error" : "DEVICE DETAILS NOT FOUND.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
                return Response({"error" : "PATIENT DETAILS NOT FOUND.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)
