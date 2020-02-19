from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(max_length = 100, required = True)
    class Meta:
        model = Patient
        fields = ['session_id', 'patient_name', 'patient_number']
        extra_kwargs =  {
                            'patient_name' : {'required' : True},
                            'patient_number' : {'required' : True}
                        }

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
