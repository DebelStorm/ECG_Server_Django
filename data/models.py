from django.db import models
from device.models import Device
from patient.models import Patient
from user_api.models import Profile
from django.utils import timezone

# Create your models here.

class Data(models.Model):
    # data_id = models.AutoField() # Auto Generated
    device_id_fk = models.ForeignKey(Device, on_delete = models.CASCADE) # or PROTECT
    user_id_fk = models.ForeignKey(Profile, on_delete = models.CASCADE) # or PROTECT
    patient_id_fk = models.ForeignKey(Patient, on_delete = models.CASCADE) # or PROTECT

    File_name = models.CharField(max_length = 100, blank=True, default='')

    Start_Time = models.TimeField(auto_now=False, auto_now_add=False, default = timezone.now)
    End_Time = models.TimeField(auto_now=False, auto_now_add=False, default = timezone.now)
