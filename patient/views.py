from django.shortcuts import render
from rest_framework import generics
from .serializers import PatientSerializer, PatientListSerializer, PatientUpdateSerializer, PatientDeleteSerializer, get_session_id_serializer, get_session_id_slno_serializer
from .models import Patient
from .permissions import AuthenticatedOnly
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from misc.models import user_patient_mapping, user_device_mapping, patient_device_mapping
from device.models import Device
from rest_framework.exceptions import ParseError

class CreatePatient(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = PatientSerializer(data = request.data)
        except ParseError:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                patient_name = serializer.validated_data.get("patient_name")
                patient_number = serializer.validated_data.get("patient_number")
                serial_number = serializer.validated_data.get("serial_number")

                device_set = Device.objects.filter(serial_number = serial_number)

                if(device_set.exists()):

                    device_obj = Device.objects.get(serial_number = serial_number)

                    user_device_set = user_device_mapping.objects.filter(user_id_fk = current_user, device_id_fk = device_obj)

                    flag = 0

                    if(user_device_set.exists()):

                        if(not Patient.objects.filter(patient_name = patient_name, patient_number = patient_number).exists()):

                            patient_obj = Patient(patient_name = patient_name, patient_number = patient_number)
                            patient_obj.save()
                        else:
                            flag += 1

                        patient_obj = Patient.objects.get(patient_name = patient_name, patient_number = patient_number)

                        user_pat_set = user_patient_mapping.objects.filter(user_id_fk = current_user, patient_id_fk = patient_obj)

                        if(not user_pat_set.exists()):

                            user_pat_map = user_patient_mapping(user_id_fk = current_user, patient_id_fk = patient_obj)
                            user_pat_map.save()
                        else:
                            flag += 1

                        device_pat_set = patient_device_mapping.objects.filter(patient_id_fk = patient_obj, device_id_fk = device_obj)

                        if(not device_pat_set.exists()):

                            device_pat_map = patient_device_mapping(patient_id_fk = patient_obj, device_id_fk = device_obj)
                            device_pat_map.save()
                        else:
                            flag += 1

                        if(flag == 3):
                            return Response({"status" : "FAIL", "error" : "ALREADY EXISTS"}, status = status.HTTP_409_CONFLICT)
                        else:
                            return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                    return Response({"error" : "USER NOT REGISTERED TO THIS DEVICE.", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

                return Response({"error" : "DEVICE DOES NOT EXIST.", "status" : "FAIL"}, status = status.HTTP_404_NOT_FOUND)

            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

class UpdatePatient(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = PatientUpdateSerializer(data = request.data)
        except ParseError:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                patient_name = serializer.validated_data.get("patient_name")
                patient_number = serializer.validated_data.get("patient_number")

                if(patient_name is not None):

                    patient_set = Patient.objects.filter(patient_number = patient_number)

                    if(patient_set.exists()):

                        patient_obj = Patient.objects.get(patient_number = patient_number)
                        user_pat_set = user_patient_mapping.objects.filter(user_id_fk = current_user, patient_id_fk = patient_obj)

                        if(user_pat_set.exists()):

                            patient_obj = Patient.objects.get(patient_number = patient_number)
                            patient_obj.patient_name = patient_name
                            patient_obj.save()

                            return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                        return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

                    return Response({"error" : "PATIENT DOES NOT EXIST", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

                return Response({"error" : "PLEASE PROVIDE DETAILS FOR UPDATE", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

class DeletePatient(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = PatientDeleteSerializer(data = request.data)
        except ParseError:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):
            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                patient_number = serializer.validated_data.get("patient_number")
                patient_set = Patient.objects.filter(patient_number = patient_number)

                if(patient_set.exists()):

                    patient_obj = Patient.objects.get(patient_number = patient_number)
                    user_pat_set = user_patient_mapping.objects.filter(user_id_fk = current_user, patient_id_fk = patient_obj)

                    if(user_pat_set.exists()):

                        patient_obj.delete()
                        return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

                    return Response({"error" : "PATIENT NOT REGISTERED TO CURRENT USER.", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

                return Response({"error" : "PATIENT DOES NOT EXIST", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

class ShowPatients(APIView):
    def post(self, request):
        try:
            serializer = get_session_id_slno_serializer(data = request.data)
        except ParseError:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):

            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                serial_number = serializer.validated_data.get("serial_number")

                json_objects = []

                device_set = Device.objects.filter(serial_number = serial_number)

                if(device_set.exists()):

                    device_obj = Device.objects.get(serial_number = serial_number)

                    if(user_device_mapping.objects.filter(user_id_fk = current_user, device_id_fk = device_obj).exists()):

                        patient_device_list = patient_device_mapping.objects.filter(device_id_fk = device_obj)

                        for device_pat_map in patient_device_list.iterator():

                            patient_obj = device_pat_map.patient_id_fk

                            return_data = {
                                'patient_number' : patient_obj.patient_number,
                                'patient_name' : patient_obj.patient_name
                            }

                            json_objects += [return_data]

                        return Response({"status" : "SUCCESS", "data" : json_objects}, status = status.HTTP_200_OK)

                    return Response({"error" : "USER NOT REGISTERED TO THIS DEVICE.", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

                return Response({"error" : "DEVICE DOES NOT EXIST.", "status" : "FAIL"}, status = status.HTTP_404_NOT_FOUND)

            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0][0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)
