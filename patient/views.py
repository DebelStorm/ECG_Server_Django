from django.shortcuts import render
from rest_framework import generics
from .serializers import PatientSerializer, PatientNoIDSerializer
from .models import Patient
from .permissions import AuthenticatedOnly
from rest_framework import permissions

class CreatePatient(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ListPatients(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class RetrieveUpdateDeletePatient(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientNoIDSerializer
    permission_classes = [permissions.IsAdminUser]

# Moved Delete Function to RetrieveUpdateDeletePatient
'''
class DeletePatient(generics.DestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permissions = [permissions.IsAuthenticated]
'''
