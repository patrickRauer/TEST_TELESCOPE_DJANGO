from django.db import models
from main.models import AbstractTelescopeDevice
# Create your models here.


class Camera(AbstractTelescopeDevice):
    pass


class Frame(models.Model):

    start_x = models.PositiveIntegerField(default=0)
    start_y = models.PositiveIntegerField(default=0)

    width = models.PositiveIntegerField(default=4096)
    height = models.PositiveIntegerField(default=4096)

    bin_x = models.PositiveSmallIntegerField(default=1)
    bin_y = models.PositiveSmallIntegerField( default=1)


class ReadOutTime(models.Model):
    """
    Stores the readout time of the frame to compute an estimated readout time in future observations
    """
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    seconds = models.FloatField()

    date = models.DateTimeField(auto_now=True)


class Image(models.Model):
    frame = models.ForeignKey(Frame, on_delete=models.SET_NULL, null=True)
    exposure_time = models.FloatField(
        default=1, help_text='Exposure time in seconds')

    dark = models.BooleanField(blank=True, default=False)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)
