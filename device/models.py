from django.db import models

# Create your models here.

class Device(models.Model):
    device_name = models.CharField(max_length = 100, blank=True, default='')
    serial_number = models.CharField(max_length = 100, blank=True, default='')
    Mac_id = models.CharField(max_length = 100, blank=True, default='')
    Num_of_Leads = models.IntegerField(default = 12)
