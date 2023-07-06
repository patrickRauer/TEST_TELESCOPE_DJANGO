from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from camera.models import Camera as CameraDB
from alpaca.camera import Camera

from mount.models import Mount
from alpaca.telescope import Telescope

from filter_wheel.models import FilterWheel as FilterWheelDB
from alpaca.filterwheel import FilterWheel
# Create your views here.


class StatusView(LoginRequiredMixin, TemplateView):
    template_name = 'status/index.html'

    def get_weather_status(self):

        return {
            'status': {
                'temperature': {
                    'in': 0,
                    'out': 0,
                },
                'humidity': {
                    'in': 10,
                    'out': 10,
                },
                'wind': {
                    'ground': 10
                }
            }
        }

    def get_filter_wheel_status(self):
        filter_wheel = FilterWheelDB.objects.last()
        filter_wheel = FilterWheel(f'{filter_wheel.ip}:{filter_wheel.port}', filter_wheel.device_id)
        position = filter_wheel.Position
        return {
            'status': {
                'position': position,
                'name': filter_wheel.Names[position]
            }
        }

    def get_camera_status(self):
        camera = CameraDB.objects.last()
        camera = Camera(f'{camera.ip}:{camera.port}', camera.device_id)

        return {
            'status':  {
                'status': camera.CameraState.__doc__,
                'temperature': camera.CCDTemperature,
                'cooler': camera.CoolerOn
            }
        }

    def get_dome_status(self):
        return {
            'status':  {
                'open': False,
                'az': '00:00:00',
            }
        }

    def hour2(self, hour_float):
        hour = int(hour_float)
        minutes = abs(hour_float-hour)*60
        seconds = int((minutes % 1) * 60)
        minutes = int(minutes)
        return f'{hour}:{minutes:02d}:{seconds:02d}'

    def degree2(self, hour_float):
        hour = int(hour_float)
        minutes = abs(hour_float-hour)*60
        seconds = int((minutes % 1) * 60)
        minutes = int(minutes)
        return f'{hour}:{minutes:02d}:{seconds:02d}'

    def get_mount_status(self):
        mount = Mount.objects.last()
        mount = Telescope(f'{mount.ip}:{mount.port}', mount.device_id)
        if not mount.Connected:
            status = 'Unconnected'
        elif mount.Tracking:
            status = 'Tracking'
        elif mount.Slewing:
            status = 'Slewing'
        elif mount.AtPark:
            status = 'Parked'
        else:
            status = 'Stopped'
        return {
            'status': {
                'status': status,
                'ra': self.hour2(mount.RightAscension),
                'dec': self.degree2(mount.Declination),
                'alt': self.hour2(mount.Altitude),
                'az': self.degree2(mount.Azimuth)
            }
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['camera'] = self.get_camera_status()
        context['mount'] = self.get_mount_status()
        context['filter_wheel'] = self.get_filter_wheel_status()
        context['dome'] = self.get_dome_status()
        context['weather'] = self.get_weather_status()
        return context
