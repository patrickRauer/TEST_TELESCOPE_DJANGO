from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from htmx.views import HTMXMixin

from filter_wheel.models import FilterWheel as FilterWheelDB
from mount.models import Mount
from .models import Camera as CameraDB, Frame, Image
from .forms import ImageForm, AbortForm

from alpaca.camera import Camera
from alpaca.filterwheel import FilterWheel
from alpaca.telescope import Telescope

# Create your views here.


class CameraIndexView(LoginRequiredMixin, HTMXMixin, TemplateView):
    template_name = ''


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


class TakeImageFormView(LoginRequiredMixin, HTMXMixin, FormView):
    template_name = 'camera/exposure/index.html'
    form_class = ImageForm

    image = None
    
    def get_success_url(self):
        image_id = self.image.id
        return reverse_lazy('camera:current_exposure', kwargs={'image_id': image_id})

    def form_valid(self, form):
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

        data = form.data
        camera.StartX = data['start_x']
        camera.StartY = data['start_y']
        camera.NumX = data['width']
        camera.NumY = data['height']
        camera.BinX = data['bin_x']
        camera.BinY = data['bin_y']
        camera.StartExposure(
            form.data['exposure_time'], 'dark' not in data
        )
        frame, _ = Frame.objects.get_or_create(
            start_x=data['start_x'], start_y=data['start_y'],
            width=data['width'], height=data['height'],
            bin_x=data['bin_x'], bin_y=data['bin_y']
        )
        self.image = Image.objects.create(
            exposure_time=data['exposure_time'],
            frame=frame,
            dark='dark' not in data
        )

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
