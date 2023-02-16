from django.db import models
from users.models import FarmUser

# Create your models here.


class Season(models.Model):

    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Crop(models.Model):

    name = models.CharField(max_length=200)
    variety = models.CharField(max_length=200)

class Farm(models.Model):

    name = models.CharField(max_length=200)
    address_line = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zip_code = models.CharField(max_length=40, blank=True)
    crop_id = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    farmer_id = models.ForeignKey(FarmUser, on_delete=models.CASCADE, null=True, blank=True)
    season_id = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
