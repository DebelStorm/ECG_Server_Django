from django.db import models
from device.models import Device
from patient.models import Patient
from user_api.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User
import os

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'DJANGO_SERVER_FILES/{0}/{1}/{2}/{3}'.format("Raw", instance.device_id_fk.serial_number, instance.patient_id_fk.patient_name, filename)

def user_directory_path_filtered(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'DJANGO_SERVER_FILES/{0}/{1}/{2}/{3}'.format("Filtered", instance.device_id_fk.serial_number, instance.patient_id_fk.patient_name, filename)

# Create your models here.

class Data(models.Model):
    # data_id = models.AutoField() # Auto Generated
    data_file_id = models.CharField(max_length = 50, unique = True)
    device_id_fk = models.ForeignKey(Device, on_delete = models.CASCADE) # or PROTECT
    user_id_fk = models.ForeignKey(User, on_delete = models.CASCADE) # or PROTECT
    patient_id_fk = models.ForeignKey(Patient, on_delete = models.CASCADE) # or PROTECT
    #File = models.FileField(upload_to = user_directory_path)
    File = models.CharField(max_length = 100)
    Start_Time = models.BigIntegerField()
    End_Time = models.BigIntegerField()

    def __str__(self):
        return 'File_ID: %s, Patient: %s , User: %s , Device: %s' % (self.data_file_id, self.patient_id_fk, self.user_id_fk, self.patient_id_fk)

class Data_filtered(models.Model):
    # data_id = models.AutoField() # Auto Generated
    data_file_id = models.CharField(max_length = 50, unique = True)
    device_id_fk = models.ForeignKey(Device, on_delete = models.CASCADE) # or PROTECT
    user_id_fk = models.ForeignKey(User, on_delete = models.CASCADE) # or PROTECT
    patient_id_fk = models.ForeignKey(Patient, on_delete = models.CASCADE) # or PROTECT
    #File = models.FileField(upload_to = user_directory_path_filtered)
    File = models.CharField(max_length = 100)
    Start_Time = models.BigIntegerField()
    End_Time = models.BigIntegerField()

    def __str__(self):
        return 'File_ID: %s, Patient: %s , User: %s , Device: %s' % (self.data_file_id, self.patient_id_fk, self.user_id_fk, self.patient_id_fk)

class BD_FE(models.Model):
    Parent_file = models.OneToOneField(Data_filtered, on_delete = models.CASCADE, primary_key = True)
    File = models.CharField(max_length = 100)

    def __str__(self):
        return 'File_ID: %s, Patient: %s , User: %s , Device: %s' % (self.Parent_file.data_file_id, self.Parent_file.patient_id_fk, self.Parent_file.user_id_fk, self.Parent_file.patient_id_fk)
