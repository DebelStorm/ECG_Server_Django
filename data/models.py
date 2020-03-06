from django.db import models
from device.models import Device
from patient.models import Patient
from user_api.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Data(models.Model):
    # data_id = models.AutoField() # Auto Generated
    data_file_id = models.CharField(max_length = 50, unique = True)
    device_id_fk = models.ForeignKey(Device, on_delete = models.CASCADE) # or PROTECT
    user_id_fk = models.ForeignKey(User, on_delete = models.CASCADE) # or PROTECT
    patient_id_fk = models.ForeignKey(Patient, on_delete = models.CASCADE) # or PROTECT
    File = models.FileField(upload_to = 'DJANGO_SERVER_FILES/')
    Start_Time = models.BigIntegerField()
    End_Time = models.BigIntegerField()

    def __str__(self):
        return 'File_ID: %s, Patient: %s , User: %s , Device: %s' % (self.data_file_id, self.patient_id_fk, self.user_id_fk, self.patient_id_fk)
