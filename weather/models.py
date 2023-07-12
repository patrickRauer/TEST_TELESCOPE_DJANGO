from django.db import models

# Create your models here.


class Page(models.Model):
    """
    :class:`Page` stores the link to the weather page
    """
    url = models.URLField(help_text="The URL of the weather page")
    date = models.DateTimeField(auto_now=True, help_text="The time of the latest change")


class Data(models.Model):
    """
    :class:`Data` stores the weather data set together with the corresponding time.
    """
    wind = models.FloatField(help_text="The wind velocity in m/s")
    wind_2m = models.FloatField(help_text="The wind velocity in m/s 2 meters above the ground")

    temperature = models.FloatField(help_text="The outside temperature")
    temperature_dome = models.FloatField(help_text="The temperature inside the dome")
    dewpoint = models.FloatField(help_text="Dewpoint ")

    humidity = models.FloatField(help_text="The outside humidity")
    humidity_dome = models.FloatField(help_text="The humidity inside the dome")

    rain = models.FloatField(help_text="Rain")

    date = models.DateTimeField(auto_now_add=True, help_text="The current time")

    def to_status(self):
        return {
            'temperature': {
                'in': self.temperature_dome,
                'out': self.temperature,
            },
            'humidity': {
                'in': self.humidity_dome,
                'out': self.humidity,
            },
            'wind': {
                'ground': self.wind,
                'h2m': self.wind_2m
            }
        }
