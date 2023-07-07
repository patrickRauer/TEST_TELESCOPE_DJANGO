from django.db import models
from main.models import AbstractTelescopeDevice
# Create your models here.


class FilterWheel(AbstractTelescopeDevice):
    pass


class Filter(models.Model):
    filter_wheel = models.ForeignKey(FilterWheel, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    letter = models.CharField(max_length=1)

    position = models.PositiveSmallIntegerField()

    flat_time = models.FloatField()

    def __str__(self):
        return f'{self.name} ({self.letter})'


class DarkImage(models.Model):
    observing_time = models.FloatField()


class MasterDark(models.Model):
    observing_time = models.FloatField()
    darks = models.ManyToManyField(DarkImage)


class FlatImage(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.SET_NULL, null=True)
    master_dark = models.ForeignKey(MasterDark, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)


class MasterFlat(models.Model):
    flats = models.ManyToManyField(FlatImage)
    created_at = models.DateTimeField(auto_now=True)
