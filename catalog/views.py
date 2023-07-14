from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from plotly import express as px
from htmx.views import HTMXMixin
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from astropy.coordinates import get_body, get_sun, get_moon
import numpy as np
import pandas as pd
from .models import CatalogItem, Location
# Create your views here.


class IndexView(LoginRequiredMixin, HTMXMixin, TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        catalog_items = CatalogItem.objects.all()
        print(self.args)
        context['catalog_items'] = catalog_items
        return context


class CatalogItemView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        return f'catalog/index/{self.request.GET.get("style", "list")}.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogItemView, self).get_context_data(**kwargs)
        catalog_items = CatalogItem.objects.all()
        context['catalog_items'] = catalog_items
        return context


class VisibilityChart(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/graphs/visibility.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ra = self.request.GET.getlist('ra')
        if len(ra) == 0:
            return context
        dec = self.request.GET.getlist('dec')
        location = Location.objects.get(pk=self.request.GET['location']) \
            if 'location' in self.request.GET else Location.objects.first()
        lat = location.latitude
        lon = location.longitude
        height = location.altitude
        ra = np.float32(ra)
        dec = np.float32(dec)
        print(ra, dec)
        coords = SkyCoord(ra*u.deg, dec*u.deg)
        location = EarthLocation(lat=lat, lon=lon, height=height)
        times = np.linspace(-12, 12, 1000)*u.hour
        times = Time.now()-times
        local_frame = AltAz(obstime=times, location=location)
        sun_alt_az = get_sun(times).transform_to(local_frame)
        moon_alt_az = get_moon(times).transform_to(local_frame)
        target = coords.transform_to(frame=local_frame)
        times = times.to_datetime()
        df = pd.concat([
            pd.DataFrame({'time': times, 'altitude': sun_alt_az.alt, 'object': ['sun']*1000}),
            pd.DataFrame({'time': times, 'altitude': moon_alt_az.alt, 'object': ['moon']*1000}),
            pd.DataFrame({'time': times, 'altitude': target.alt, 'object': ['target']*1000}),
        ])
        fig = px.line(df, 'time', 'altitude', color='object')
        fig.update_layout(
            {
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font_color': 'rgba(220, 220, 220, 0.8)'
            }
        )
        context['graph'] = fig.to_json()
        return context
