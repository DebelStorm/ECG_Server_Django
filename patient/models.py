from django.db import models

# Create your models here.

class Patient(models.Model):
    patient_name = models.CharField(max_length = 100, blank=True, default='')
    patient_number = models.CharField(max_length = 50, unique = True, blank=True, default='')
    def __str__(self):
        return self.patient_name
