from django.db import models

# Create your models here.


class Dome(models.Model):
    name = models.CharField(max_length=50)
    azimuth_limit = models.FloatField(
        help_text='Maximal limit after which the dome is moved actively to be aligned with the mount in degrees'
    )
    auto_alignment = models.BooleanField(default=True, help_text='True, if the dome should be aligned actively'
                                                                 'with the mount, else False.')
