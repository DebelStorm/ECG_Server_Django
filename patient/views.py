from django.shortcuts import render
from rest_framework import generics
from .serializers import PatientSerializer, PatientNoIDSerializer
from .models import Patient
from .permissions import AuthenticatedOnly
from rest_framework import permissions

# Create your views here.

class CreatePatient(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permissions = [permissions.IsAuthenticated, AuthenticatedOnly]

class ListPatients(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permissions = [permissions.IsAuthenticated, AuthenticatedOnly]

class RetrieveUpdateDeletePatient(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientNoIDSerializer
    permissions = [permissions.IsAuthenticated, AuthenticatedOnly]

# Moved Delete Function to RetrieveUpdateDeletePatient
'''
class DeletePatient(generics.DestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permissions = [permissions.IsAuthenticated]
'''
