from django.db import models

# Create your models here.


class AbstractTelescopeDevice(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=40, help_text='Name of the device')
    ip = models.GenericIPAddressField(help_text='Static IP of the device')
    port = models.PositiveSmallIntegerField(default=32323, help_text='Used port of the device')

    device_id = models.PositiveSmallIntegerField(help_text='Device ID of the device')