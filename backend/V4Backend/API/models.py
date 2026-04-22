import uuid

from django.db import models

# Create your models here.
class Polygon(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    polygon_id = models.CharField()