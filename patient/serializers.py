from rest_framework import serializers
from .models import Patient

class AddPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['serial_number']
