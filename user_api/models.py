from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(blank = True, default = '', max_length = 20)
    OTP = models.CharField(blank = False, default = '000000', max_length = 6)

    def __str__(self):
        return self.user
