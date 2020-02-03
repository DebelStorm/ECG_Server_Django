from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'patient_name', 'patient_number']

class PatientNoIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [ 'patient_name', 'patient_number']
