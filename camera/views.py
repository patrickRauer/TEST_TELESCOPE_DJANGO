import time

from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from htmx.views import HTMXMixin
from plotly import express as px
import pandas as pd

from filter_wheel.models import FilterWheel as FilterWheelDB
from mount.models import Mount
from .models import Camera as CameraDB, Frame, ImageSettings, Image, Temperature
from .forms import ImageForm, AbortForm, CameraForm, CoolerForm
from .tasks import perform_exposures

from alpaca.camera import Camera
from alpaca.filterwheel import FilterWheel
from alpaca.telescope import Telescope

# Create your views here.


class CameraIndexView(LoginRequiredMixin, HTMXMixin, FormView):
    template_name = 'camera/index/index.html'
    form_class = CameraForm
    success_url = reverse_lazy('camera:index')
    camera_entry = None
    
    def dispatch(self, request, *args, **kwargs):
        self.camera_entry = CameraDB.objects.last()
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'id': self.camera_entry.id,
            'name': self.camera_entry.name,
            'ip': self.camera_entry.ip,
            'port': self.camera_entry.port,
            'device_id': self.camera_entry.device_id
        }

    def form_valid(self, form):
        self.camera_entry.name = form.data['name']
        self.camera_entry.ip = form.data['ip']
        self.camera_entry.port = form.data['port']
        self.camera_entry.device_id = form.data['device_id']
        self.camera_entry.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cooler'] = {
            'form': CoolerForm()
        }
        return context


class CameraStatusView(LoginRequiredMixin, HTMXMixin, TemplateView):
    template_name = 'camera/status/index.html'

    def get_context_data(self, **kwargs):
        camera = CameraDB.objects.last()
        camera = Camera(f'{camera.ip}:{camera.port}', camera.device_id)

        context = super().get_context_data(**kwargs)
        context['camera'] = {
            'status':  {
                'status': camera.CameraState.__doc__,
                'temperature': camera.CCDTemperature,
                'cooler': camera.CoolerOn
            }
        }
        return context


class CameraTemperatureView(LoginRequiredMixin, TemplateView):
    template_name = 'camera/index/graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        df = pd.DataFrame(
            Temperature.objects.filter(date__gte=timezone.now()-timezone.timedelta(days=1)).values('date', 'temperature')
        )
        if len(df) == 0:
            return context
        fig = px.scatter(df, 'date', 'temperature')
        fig.data[0].update(mode='markers+lines')
        fig.update_layout(
            {
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            }
        )
        context['graph'] = fig.to_json()
        return context


class TakeImageFormView(LoginRequiredMixin, HTMXMixin, FormView):
    template_name = 'camera/exposure/index.html'
    form_class = ImageForm

    image = None
    
    def get_success_url(self):
        image_id = self.image.id
        return reverse_lazy('camera:current_exposure', kwargs={'image_id': image_id})

    def form_valid(self, form: ImageForm):
        filter_wheel = FilterWheelDB.objects.last()
        filter_wheel = FilterWheel(f'{filter_wheel.ip}:{filter_wheel.port}', filter_wheel.device_id)
        if filter_wheel.Position == -1:
            return HttpResponse(b'Filter wheel moving', status=400)

        mount = Mount.objects.last()
        telescope = Telescope(f'{mount.ip}:{mount.port}', mount.device_id)
        if telescope.Slewing:
            return HttpResponse(b'Telescope slewing', status=400)

        camera = CameraDB.objects.last()
        camera = Camera(f'{camera.ip}:{camera.port}', camera.device_id)
        if camera.CameraState != 0:
            return HttpResponse(b'Camera is busy', status=400)

        data = form.cleaned_data
        frame, _ = Frame.objects.get_or_create(
            start_x=data['start_x'], start_y=data['start_y'],
            width=data['width'], height=data['height'],
            bin_x=data['bin_x'], bin_y=data['bin_y']
        )
        self.image = ImageSettings.objects.create(
            exposure_time=data['exposure_time'],
            frame=frame,
            filter=data['filter'],
            repeats=data['repeats'],
            dark='dark' not in data,
            observer=self.request.user
        )
        perform_exposures.delay(self.image.id)
        return super().form_valid(form)


class CurrentExposureView(LoginRequiredMixin, HTMXMixin, FormView):
    template_name = 'camera/current_exposure/index.html'
    form_class = AbortForm

    def get_success_url(self):
        return ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = Image.objects.get(pk=self.kwargs['image_id'])
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return form
