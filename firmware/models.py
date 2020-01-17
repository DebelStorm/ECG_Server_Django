from django.db import models
from device.models import Device

# Create your models here.

class Firmware_Version(models.Model):
    device_id_fk = models.ForeignKey(Device, on_delete=models.CASCADE)
    Firmware_Version_id = models.CharField(max_length = 100, blank = True, default = ' -- ')
    Firmware_version_number = models.CharField(max_length = 100, blank = True, default = ' -- ')
