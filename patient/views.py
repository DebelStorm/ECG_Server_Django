from django.shortcuts import render
from rest_framework import generics
from .serializers import PatientSerializer, PatientListSerializer
from .models import Patient
from .permissions import AuthenticatedOnly
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions, status

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

                return Response("SUCCESS", status = status.HTTP_200_OK)

            return Response("INVALID TOKEN", status = status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ListPatients(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    #permission_classes = [permissions.IsAuthenticated]


# PATIENT DELETE, UPDATE IN PROGRESS
'''
class RetrieveUpdateDeletePatient(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientNoIDSerializer
    #permission_classes = [permissions.IsAdminUser]

# Moved Delete Function to RetrieveUpdateDeletePatient

class DeletePatient(generics.DestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permissions = [permissions.IsAuthenticated]
'''
