from django.db import models
from django.contrib.auth import get_user_model
from main.models import AbstractTelescopeDevice
from filter_wheel.models import Filter
# Create your models here.


User = get_user_model()


class Camera(AbstractTelescopeDevice):
    pass


class Temperature(models.Model):
    temperature = models.FloatField()
    cooler_on = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)


class Frame(models.Model):

    start_x = models.PositiveIntegerField(default=0)
    start_y = models.PositiveIntegerField(default=0)

    width = models.PositiveIntegerField(default=4096)
    height = models.PositiveIntegerField(default=4096)

    bin_x = models.PositiveSmallIntegerField(default=1)
    bin_y = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'x0: {self.start_x}, y0: {self.start_y}, width: {self.width}, height: {self.height} ' \
               f'bin: ({self.bin_x}, {self.bin_y})'


class ReadOutTime(models.Model):
    """
    Stores the readout time of the frame to compute an estimated readout time in future observations
    """
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    seconds = models.FloatField()

    date = models.DateTimeField(auto_now=True)


class AbstractImage(models.Model):
    class Meta:
        abstract = True

    frame = models.ForeignKey(Frame, on_delete=models.SET_NULL, null=True)
    exposure_time = models.FloatField(
        default=1, help_text='Exposure time in seconds')
    filter = models.ForeignKey(Filter, on_delete=models.SET_NULL, null=True)

    dark = models.BooleanField(blank=True, default=False)

    observer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)


class Image(AbstractImage):
    fits_file = models.FileField(null=True)

    def to_fits_header(self):
        return {
            'frame': f'[{self.frame.start_x},{self.frame.start_y};{self.frame.width},{self.frame.height}]',
            'filter': self.filter.name,
            'imagetype': 'science',
            'filter_letter': self.filter.letter,
            'observer': self.observer.username,
            'obs_time': '',
            'obs_local_start': str(self.started_at),
            'obs_local_end': str(self.finished_at),
            'exposure_time': self.exposure_time,

        }


class ImageSettings(AbstractImage):
    repeats = models.PositiveSmallIntegerField(default=1)
    images_done = models.PositiveSmallIntegerField(default=0)

