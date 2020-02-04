from django import forms
from .models import Data

class DataUploadForm(forms.ModelForm):
    device_sl_no = forms.CharField(max_length = 100, required = True)
    patient_no = forms.CharField(max_length = 100, required = True)
    File = forms.FileField(required = True)
    Start_Time = forms.TimeField()
    End_Time = forms.TimeField()
