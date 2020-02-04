from django.shortcuts import render
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view
from .forms import DataUploadForm
from .serializers import DataUploadSerializer
from rest_framework.views import APIView
from device.models import Device
from patient.models import Patient
from .models import Data
from rest_framework import status

# Create your views here.

class post_data_forms(APIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser, )
    def post(self, request, *args, **kwargs):
        if(not request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = DataUploadSerializer(data = request.data)
        current_user = request.user
        if(Device.objects.filter(serial_number = serializer.validated_data.get('device_sl_no')).exists() and Patient.objects.get(patient_number = serializer.validated_data.get('patient_no')).exists()):
            current_device = Device.objects.get(serial_number = serializer.validated_data.get('device_sl_no'))
            current_patient = Patient.objects.get(patient_number = serializer.validated_data.get('patient_no'))

            new_file = Data(device_id_fk = current_device, user_id_fk = current_user, patient_id_fk = current_patient, File = serializer.validated_data.get('File'), Start_Time = serializer.validated_data.get('Start_Time'), End_Time = serializer.validated_data.get('End_Time'))
            new_file.save()

            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)

'''
@api_view(['POST'])
def post_data_forms(request):
    if(not request.user.is_authenticated):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        if(request.method == "POST"):
            formData = DataUploadForm(request.POST,request.FILES)
            if(formData.is_valid()):
                form.save()
                return Response(status = status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST)
'''
