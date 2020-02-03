from django.db import models
from device.models import Device

# Create your models here.

class Firmware_Version(models.Model):
    device_id_fk = models.ForeignKey(Device, on_delete=models.CASCADE)
    Firmware_Version_id = models.CharField(max_length = 100, blank = True, default = ' N/A ')
    Firmware_version_number = models.CharField(max_length = 100, blank = True, default = ' N/A ')

    def __str__(self):
        return '%s - %s' % (self.device_id_fk, self.Firmware_Version_id)
