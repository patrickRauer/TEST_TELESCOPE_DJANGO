from django.db import models
from filter_wheel.models import Filter
# Create your models here.


class Type(models.Model):
    """
    Astronomical type
    """
    name = models.CharField(max_length=40, help_text='Name of the type like "Exoplanet", "QSO" and so on')


class Target(models.Model):
    """
    Astronomical target with coordinates and type
    """
    name = models.CharField(max_length=100, blank=True, default='', help_text='Name of the target')
    description = models.TextField(blank=True, default='', help_text='Additional description of the target')
    ra = models.FloatField(help_text='RA in hour float')
    dec = models.FloatField(help_text='Dec in degrees')
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        null=True,
        help_text='The type of the target'
    )


class CatalogItem(models.Model):
    """
    Entry for predefined observation, which can be used to start an observation quick.
    """
    name = models.CharField(max_length=100, help_text='Name of the catalog entry')
    target = models.ForeignKey(
        Target,
        on_delete=models.SET_NULL,
        null=True, help_text='The target for this catalog entry'
    )
    filter = models.ForeignKey(Filter, on_delete=models.SET_NULL, null=True, help_text='The to used filter')

    exposure_time = models.FloatField(help_text='The exposure time in seconds')
    capture = models.ImageField(null=True, blank=True, help_text='Preview of the target')

    created_at = models.DateTimeField(auto_now=True, help_text='The datetime when the entry was created')
    updated_at = models.DateTimeField(
        auto_now_add=True,
        help_text='The datetime when the entry was updated the last time'
    )
