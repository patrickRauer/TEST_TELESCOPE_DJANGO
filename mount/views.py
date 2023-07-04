from django.views.generic import TemplateView, FormView
from django.conf import settings
from htmx.views import HTMXMixin
from .forms import SlewForm, ParkForm
from .models import Coordinate

from alpaca.telescope import Telescope
# Create your views here.


class IndexView(HTMXMixin, TemplateView):
    template_name = 'mount/index/index.html'


class SlewFormView(HTMXMixin, FormView):
    template_name = 'mount/slew/index.html'
    form_class = SlewForm

    def get_success_url(self):
        return ''

    def to_hour(self, value: str):
        if not isinstance(value, str):
            return value
        if ':' in value or 'h' in value:
            if ':' in value:
                value = value.split(':')
                value = float(value[0])+float(value[1])/60+float(value[2])/3600
            else:
                hour, rest = value.split('h')
                minute, second = rest.split('m')
                second = second.strip('s')
                value = float(hour)+float(minute)/60+float(second)/3600
        else:
            try:
                value = float(value)
            except TypeError:
                raise ValueError('Unknown coordinate format')
        return value

    def to_degree(self, value: str):
        if not isinstance(value, str):
            return value
        if ':' in value or 'd' in value:
            if ':' in value:
                value = value.split(':')
                value = float(value[0])+float(value[1])/60+float(value[2])/3600
            else:
                hour, rest = value.split('d')
                minute, second = rest.split('m')
                second = second.strip('s')
                value = float(hour)+float(minute)/60+float(second)/3600
        else:
            try:
                value = float(value)
            except TypeError:
                raise ValueError('Unknown coordinate format')
        return value

    def form_valid(self, form):
        mount = Telescope(settings.MOUNT_IP_PORT, 0)
        if mount.Slewing:
            form.add_error('ra', 'Telescope is already slewing')
            return self.form_invalid(form)
        if mount.AtPark:
            mount.Unpark()
        mount.Tracking = True
        ra = self.to_hour(form.data['ra'])
        dec = self.to_degree(form.data['dec'])
        mount.SlewToCoordinatesAsync(ra, dec)

        Coordinate.objects.create(ra=ra, dec=dec)

        response = super().form_valid(form)
        return response


class ParkFormView(HTMXMixin, FormView):
    template_name = 'mount/park/index.html'
    form_class = ParkForm

    def get_success_url(self):
        return ''

    def form_valid(self, form):
        mount = Telescope(settings.MOUNT_IP_PORT, 0)
        mount.Park()
        response = super().form_valid(form)
        return response


class StatusView(TemplateView):
    template_name = 'mount/status/index.html'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mount = Telescope(settings.MOUNT_IP_PORT, 0)
        if not mount.Connected:
            status = 'Unconnected'
        elif mount.Tracking:
            status = 'Tracking'
        elif mount.Slewing:
            status = 'Slewing'
        elif mount.AtPark:
            status = 'Parked'
        else:
            status = 'Unknown'
        context['status'] = status
        context['ra'] = self.hour2(mount.RightAscension)
        context['dec'] = self.degree2(mount.Declination)
        context['alt'] = self.hour2(mount.Altitude)
        context['az'] = self.degree2(mount.Azimuth)
        return context
