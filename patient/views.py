from django.shortcuts import render
from rest_framework import generics
from .serializers import PatientSerializer, PatientListSerializer, PatientUpdateSerializer, PatientDeleteSerializer, get_session_id_serializer
from .models import Patient
from .permissions import AuthenticatedOnly
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from misc.models import user_patient_mapping
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

                patient_obj = Patient(patient_name = patient_name, patient_number = patient_number)
                patient_obj.save()

                user_pat_set = user_patient_mapping.objects.filter(user_id_fk = current_user, patient_id_fk = patient_obj)

                if(not user_pat_set.exists()):

                    user_pat_map = user_patient_mapping(user_id_fk = current_user, patient_id_fk = patient_obj)
                    user_pat_map.save()

                return Response({"status" : "SUCCESS"}, status = status.HTTP_200_OK)

            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0]
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
        error_value = list(serializer.errors.values())[0]
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

                    return Response({"error" : "UNAUTHORIZED", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

                return Response({"error" : "PATIENT DOES NOT EXIST", "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status = status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)

class ShowPatients(APIView):
    def post(self, request):
        try:
            serializer = get_session_id_serializer(data = request.data)
        except ParseError:
            return Response({"error" : "JSON PARSE ERROR", "status" : "FAIL"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if(serializer.is_valid()):

            session_id = serializer.validated_data.get("session_id")
            token_set = Token.objects.filter(key = session_id)

            if(token_set.exists()):

                token_object = Token.objects.get(key = session_id)
                current_user = token_object.user

                user_patient_list = user_patient_mapping.objects.filter(user_id_fk = current_user)

                json_objects = []

                for user_pat_map in user_patient_list.iterator():

                    patient_obj = user_pat_map.patient_id_fk

                    return_data = {
                        'patient_number' : patient_obj.patient_number,
                        'patient_name' : patient_obj.patient_name
                    }

                    json_objects += [return_data]

                return Response({"status" : "SUCCESS", "data" : json_objects}, status = status.HTTP_200_OK)

            return Response({"error" : "INVALID TOKEN", "status" : "FAIL"}, status=status.HTTP_401_UNAUTHORIZED)

        error_key = list(serializer.errors.keys())[0]
        error_value = list(serializer.errors.values())[0]
        error_string = str(error_key) + " : " + str(error_value)
        return Response({"error" : error_string, "status" : "FAIL"}, status = status.HTTP_400_BAD_REQUEST)
