from django.shortcuts import render
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view
from .forms import DataUploadForm
from .serializers import DataUploadSerializer, DataDownloadSerializer, DataUploadSerializerJSON, BDFE_DataUploadSerializer
from rest_framework.views import APIView
from device.models import Device
from patient.models import Patient
from .models import Data, Data_filtered, BD_FE
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
def merge_array(a):
    final_a = []
    for signal_number in range(12):
        signal = []
        for file_number in range(len(a)):
            if(a[file_number]):
                signal += a[file_number][signal_number]
        final_a += [signal]
    return final_a

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

class post_bdfe(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = BDFE_DataUploadSerializer(data = request.data)
        except ParseError:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):

            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                File_location = serializer.validated_data.get("File_location")
                data_id = serializer.validated_data.get("data_id")
                overwrite = serializer.validated_data.get("overwrite")

                if(not path.exists(File_location)):
                    return Response({"error" : "File location invalid. File not found at given file locaition.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)

                if(Data_filtered.objects.filter(data_file_id = data_id).exists()):

                    Parent_file = Data_filtered.objects.get(data_file_id = data_id)

                    if not BD_FE.objects.filter(Parent_file = Parent_file).exists():

                        BD_FE_new_Object = BD_FE(Parent_file = Parent_file, File = File_location)
                        BD_FE_new_Object.save()

                        return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                    elif(overwrite):

                        BD_FE_new_Object = BD_FE.objects.get(Parent_file = Parent_file)
                        BD_FE_new_Object.File = File_location
                        BD_FE_new_Object.save()

                        return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                    return Response({"error" : "FILE ALREADY EXISTS", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

                return Response({"error" : "PARENT FILE DOES NOT EXISTS", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

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
                get_bdfe = serializer.validated_data.get("get_bdfe")

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
                get_bdfe = serializer.validated_data.get("get_bdfe")
                download_mode = serializer.validated_data.get("download_mode")
                include_bdfe_index = serializer.validated_data.get("include_bdfe_index")
                show_all_averages = serializer.validated_data.get("show_all_averages")

                if download_mode is None or download_mode < 0 or download_mode > 1 :
                    download_mode = 0

                if include_bdfe_index is None or include_bdfe_index < 0 or include_bdfe_index > 1:
                    include_bdfe_index = 0

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

                            Boundaries = []
                            R_peaks = []
                            P_Wave = []
                            QRS_Wave = []
                            T_Wave = []
                            avg_P = []
                            avg_QRS = []
                            avg_T = []
                            avg_PR = []
                            avg_QT = []
                            avg_QTc = []
                            avg_HRV = []
                            BPM = []

                            BDFE_flags = [0 for temp_count in range(len(data_files_objects))]

                            Current_starttime = 0
                            Current_endtime = 0
                            server_unavailability_flag = 0
                            time_unavailability_flag = 0
                            BDFE_unavailability_flag = 0
                            count = 0
                            BDFE_index = 0

                            for data_file_object in data_files_objects:

                                Current_File_path = data_file_object.File

                                BDFE_obj = None
                                if(BD_FE.objects.filter(Parent_file = data_file_object).exists()):
                                    BDFE_obj = BD_FE.objects.get(Parent_file = data_file_object)

                                if(not path.exists(Current_File_path)):
                                    server_unavailability_flag = 1

                                else:

                                    # Process the file
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
                                        Current_endtime = End_Time_of_Current_File
                                        count += 1
                                    elif(count == 1):
                                        if(Start_Time_of_Current_File != Current_endtime):
                                            time_unavailability_flag = 1
                                            count += 1
                                        Current_endtime = End_Time_of_Current_File
                                        Current_starttime = Start_Time_of_Current_File

                                    # Process the BDFE file if required

                                    if(download_mode):

                                        try:

                                            Current_BDFE_File_path = BDFE_obj.File

                                            if(path.exists(Current_BDFE_File_path)):

                                                Current_File = io.open(Current_BDFE_File_path, encoding = 'utf8')
                                                content = str(Current_File.read()).split("\n")
                                                content = csv.reader(content, delimiter = ",")
                                                content = [x for x in content if x != []]
                                                no_of_rows_current_file = len(content)
                                                content = np.asarray(content).T.tolist()

                                                for i in range(len(content)):
                                                    content[i] = [int(float(x)) for x in content[i] if x != ''] # Converted to int, Later to be changed to str
                                                    content[i] = [x for x in content[i] if x <= 10000 and x >= 0] # Bound Check Condition

                                                Boundaries += [content[:12]]
                                                R_peaks += [content[12:24]]
                                                P_Wave += [content[24:36]]
                                                QRS_Wave += [content[36:48]]
                                                T_Wave += [content[48:60]]

                                                avg_P += [content[60]]
                                                avg_QRS += [content[61]]
                                                avg_T += [content[62]]
                                                avg_PR += [content[63]]
                                                avg_QT += [content[64]]
                                                avg_QTc += [content[65]]
                                                avg_HRV += content[66]
                                                BPM += content[67]

                                                BDFE_flags[BDFE_index] = 1

                                        except:

                                            pass
                                            Boundaries += [[]]
                                            R_peaks += [[]]
                                            P_Wave += [[]]
                                            QRS_Wave += [[]]
                                            T_Wave += [[]]
                                            BDFE_unavailability_flag = 1
                                            #avg_P += [[]]
                                            #avg_QRS += [[]]
                                            #avg_T += [[]]
                                            #avg_PR += [[]]
                                            #avg_QT += [[]]
                                            #avg_QTc += [[]]
                                            #avg_HRV += [[]]
                                            #BPM += [[]]

                                BDFE_index += 1

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

                            File_Length = 10000

                            start_time_slice = round((Start_Time - Start_Time_set[0]) * frequency)
                            end_time_slice = round((End_Time_set[-1] - End_Time) * frequency)

                            if(no_of_files_var > 0):

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

                            if len(End_Time_set) > 0 and End_Time_set[-1] != End_Time :
                                 time_unavailability_flag = 1

                            if len(Start_Time_set) > 0 and Start_Time_set[0] != Start_Time :
                                 time_unavailability_flag = 1

                            response = {
                                'status' : 'SUCCESS',
                                'no_of_files' : no_of_files_var,
                                'Start_Time_set' : Start_Time_set,
                                'End_Time_set' : End_Time_set,
                                'No_of_records' : no_of_rows,
                                'Data' : final_data,
                            }

                            if(download_mode):

                                # Send the BDFE Values in proper Format

                                # Adjust to match appended length
                                #temp_count = 0
                                for i in range(len(BDFE_flags)):
                                    if(BDFE_flags[i]):
                                        for j in range(12):
                                            Boundaries[i][j] = [value + File_Length*i for value in Boundaries[i][j]]
                                            R_peaks[i][j] = [value + File_Length*i for value in R_peaks[i][j]]
                                            P_Wave[i][j] = [value + File_Length*i for value in P_Wave[i][j]]
                                            QRS_Wave[i][j] = [value + File_Length*i for value in QRS_Wave[i][j]]
                                            T_Wave[i][j] = [value + File_Length*i for value in T_Wave[i][j]]
                                        #temp_count += 1

                                # Append each BDFE parameter
                                rPeakMaxLength = 0

                                if(len(Boundaries)):
                                    Boundaries = merge_array(Boundaries)
                                    R_peaks = merge_array(R_peaks)
                                    P_Wave = merge_array(P_Wave)
                                    QRS_Wave = merge_array(QRS_Wave)
                                    T_Wave = merge_array(T_Wave)

                                    rPeakMaxLength = max([len(array) for array in R_peaks])
                                # Slice first and last parts of BDFE and adjust accordingly
                                try:
                                    if(start_time_slice > 0):
                                        for i in range(len(Boundaries)):
                                            Boundaries[i] = [value - start_time_slice for value in Boundaries[i] if value > start_time_slice]
                                            R_peaks[i] = [value - start_time_slice for value in R_peaks[i] if value > start_time_slice]
                                            P_Wave[i] = [value - start_time_slice for value in P_Wave[i] if value > start_time_slice]
                                            QRS_Wave[i] = [value - start_time_slice for value in QRS_Wave[i] if value > start_time_slice]
                                            T_Wave[i] = [value - start_time_slice for value in T_Wave[i] if value > start_time_slice]

                                    if(not R_peaks):
                                        avg_HRV = []
                                    else:
                                        newRPeakMaxLength = max([len(array) for array in R_peaks])
                                        avg_HRV = avg_HRV[rPeakMaxLength - newRPeakMaxLength : ]
                                        rPeakMaxLength = newRPeakMaxLength

                                    if(end_time_slice > 0):
                                        if(start_time_slice > 0):
                                            for i in range(len(Boundaries)):
                                                Boundaries[i] = [value for value in Boundaries[i] if value + start_time_slice < no_of_files_var*File_Length - end_time_slice]
                                                R_peaks[i] = [value for value in R_peaks[i] if value + start_time_slice < no_of_files_var*File_Length - end_time_slice]
                                                P_Wave[i] = [value for value in P_Wave[i] if value + start_time_slice < no_of_files_var*File_Length - end_time_slice]
                                                QRS_Wave[i] = [value for value in QRS_Wave[i] if value + start_time_slice < no_of_files_var*File_Length - end_time_slice]
                                                T_Wave[i] = [value for value in T_Wave[i] if value + start_time_slice < no_of_files_var*File_Length - end_time_slice]
                                        else:
                                            for i in range(len(Boundaries)):
                                                Boundaries[i] = [value for value in Boundaries[i] if value < no_of_files_var*File_Length - end_time_slice]
                                                R_peaks[i] = [value for value in R_peaks[i] if value < no_of_files_var*File_Length - end_time_slice]
                                                P_Wave[i] = [value for value in P_Wave[i] if value < no_of_files_var*File_Length - end_time_slice]
                                                QRS_Wave[i] = [value for value in QRS_Wave[i] if value < no_of_files_var*File_Length - end_time_slice]
                                                T_Wave[i] = [value for value in T_Wave[i] if value < no_of_files_var*File_Length - end_time_slice]

                                    if(not R_peaks):
                                        avg_HRV = []
                                    else:
                                        newRPeakMaxLength = max([len(array) for array in R_peaks])
                                        if((rPeakMaxLength - newRPeakMaxLength) > 0):
                                            avg_HRV = avg_HRV[: -(rPeakMaxLength - newRPeakMaxLength)]
                                        rPeakMaxLength = newRPeakMaxLength
                                except:
                                    pass

                                # Push the values to response

                                if(include_bdfe_index):
                                    response['Boundaries'] = Boundaries
                                    response['R_peaks'] = R_peaks
                                    response['P_Wave'] = P_Wave
                                    response['QRS_Wave'] = QRS_Wave
                                    response['T_Wave'] = T_Wave

                                avgp = [int(np.mean(x)) for x in np.asarray(avg_P).T.tolist()]
                                avgqrs = [int(np.mean(x)) for x in np.asarray(avg_QRS).T.tolist()]
                                avgt = [int(np.mean(x)) for x in np.asarray(avg_T).T.tolist()]
                                avgpr = [int(np.mean(x)) for x in np.asarray(avg_PR).T.tolist()]
                                avgqt = [int(np.mean(x)) for x in np.asarray(avg_QT).T.tolist()]
                                avgqtc = [int(np.mean(x)) for x in np.asarray(avg_QTc).T.tolist()]

                                response['avg_P'] = [int(np.mean(avgp))] + avgp
                                response['avg_QRS'] = [int(np.mean(avgqrs))] + avgqrs
                                response['avg_T'] = [int(np.mean(avgt))] + avgt
                                response['avg_PR'] = [int(np.mean(avgpr))] + avgpr
                                response['avg_QT'] = [int(np.mean(avgqt))] + avgqt
                                response['avg_QTc'] = [int(np.mean(avgqtc))] + avgqtc


                                response['HRV'] = avg_HRV
                                response['BPM'] = BPM
                                response['BDFE_flags'] = BDFE_flags
                                response['start_time_slice'] = start_time_slice
                                response['end_time_slice'] = end_time_slice

                            if(server_unavailability_flag):
                                response['message'] = 'Only partial data available. Some files missing in server. '
                            elif(time_unavailability_flag):
                                response['message'] = 'Only partial data available. Files not available for some time periods. '
                            else:
                                response['message'] = 'All filtered files for the given time stamp available. '

                            if(BDFE_unavailability_flag):
                                response['message'] += 'BD-FE analysis not available for some files. '

                            return Response(response, status = status.HTTP_200_OK)

                        return Response({"error" : "NO RECORDS FOUND FOR THE GIVEN TIME PERIOD.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
                    return Response({"error" : "DEVICE DETAILS NOT FOUND.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
                return Response({"error" : "PATIENT DETAILS NOT FOUND.", "status" : "FAIL"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)
