from django.db import models

from device.models import Device
from patient.models import Patient
from user_api.models import Profile

# Create your models here.

class user_device_mapping(models.Model):
    # id = models.AutoField()
    device_id_fk = models.ForeignKey(Device, on_delete = models.CASCADE) # or PROTECT
    user_id_fk = models.ForeignKey(Profile, on_delete = models.CASCADE) # or PROTECT
