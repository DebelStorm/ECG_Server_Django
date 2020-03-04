from django.contrib import admin
from .models import user_device_mapping, user_patient_mapping

# Register your models here.

admin.site.register(user_device_mapping)
admin.site.register(user_patient_mapping)
