from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

USER_TYPE_CHOICES = [
    ('admin', 'Admin'),
    ('farmer', 'Farmer')
]

class FarmUser(AbstractUser):
    
    user_type = models.CharField(max_length=40,choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True)
    email = models.CharField(max_length=40, blank=True)
    address_line = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zip_code = models.CharField(max_length=40, blank=True)
    mobile = models.CharField(max_length=40, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
