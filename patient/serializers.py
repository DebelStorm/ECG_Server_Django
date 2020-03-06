from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    serial_number = serializers.CharField(max_length = 100, required = True)
    patient_name = serializers.CharField(max_length = 100, required = True)
    patient_number = serializers.CharField(max_length = 100, required = True)

class PatientUpdateSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    patient_name = serializers.CharField(max_length = 100)
    patient_number = serializers.CharField(max_length = 100, required = True)

class PatientDeleteSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    patient_number = serializers.CharField(max_length = 100, required = True)

class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_name', 'patient_number']

class get_session_id_serializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)

class get_session_id_slno_serializer(serializers.Serializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    serial_number = serializers.CharField(max_length = 100, required = True)
