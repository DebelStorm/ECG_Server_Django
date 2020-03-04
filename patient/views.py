from django.shortcuts import render
from rest_framework import generics
from .serializers import PatientSerializer, PatientListSerializer, PatientUpdateSerializer, PatientDeleteSerializer
from .models import Patient
from .permissions import AuthenticatedOnly
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from misc.models import user_patient_mapping

class CreatePatient(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PatientSerializer(data = request.data)
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

                user_pat_set = user_patient_mapping.objects.filter(user_id_fk = current_user, patient_id_fk = current_user)

                if(not user_pat_set.exists()):

                    user_pat_map = user_patient_mapping(user_id_fk = current_user, patient_id_fk = patient_obj)
                    user_pat_map.save()

                return Response("SUCCESS", status = status.HTTP_200_OK)

            return Response("INVALID TOKEN", status = status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UpdatePatient(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PatientUpdateSerializer(data = request.data)
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

                        user_pat_set = user_patient_mapping.objects.filter(user_id_fk = current_user, patient_id_fk = current_user)

                        if(user_pat_set.exists()):

                            patient_obj = Patient.objects.get(patient_number = patient_number)
                            patient_obj.patient_name = patient_name
                            patient_obj.save()

                            return Response("SUCCESS", status = status.HTTP_200_OK)

                        return Response("UNAUTHORIZED", status = status.HTTP_401_UNAUTHORIZED)

                    return Response("PATIENT DOES NOT EXIST", status = status.HTTP_400_BAD_REQUEST)

                return Response("PLEASE PROVIDE DETAILS FOR UPDATE", status = status.HTTP_400_BAD_REQUEST)

            return Response("INVALID TOKEN", status = status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DeletePatient(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PatientDeleteSerializer(data = request.data)
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
                    user_pat_set = user_patient_mapping.objects.filter(user_id_fk = current_user, patient_id_fk = current_user)

                    if(user_pat_set.exists()):

                        patient_obj.delete()
                        return Response("SUCCESS", status = status.HTTP_200_OK)

                    return Response("UNAUTHORIZED", status = status.HTTP_401_UNAUTHORIZED)

                return Response("PATIENT DOES NOT EXIST", status = status.HTTP_400_BAD_REQUEST)

            return Response("INVALID TOKEN", status = status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ShowPatients(APIView):
    def get(self, request):
        pass
