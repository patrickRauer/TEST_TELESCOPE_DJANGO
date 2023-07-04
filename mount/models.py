from django.db import models
from main.models import AbstractTelescopeDevice
# Create your models here.


class Mount(AbstractTelescopeDevice):
    pass


class Coordinate(models.Model):
    ra = models.FloatField()
    dec = models.FloatField()

    date = models.DateTimeField(auto_now_add=True)
