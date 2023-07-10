from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from htmx.views import HTMXMixin

from .forms import ObservationForm
from mount.forms import SlewForm
from camera.forms import ImageForm
from camera.models import Image, ImageSettings
from camera.views import TakeImageFormView


# Create your views here.
class IndexView(LoginRequiredMixin, HTMXMixin, TemplateView):
    template_name = 'observation/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slew'] = {'form': SlewForm()}
        context['image'] = {'form': ImageForm()}
        return context


class StartExposureFormView(TakeImageFormView):
    template_name = 'observation/exposure/index.html'

    def get_success_url(self):
        image_id = self.image.id
        return reverse_lazy('observation:running_exposure', kwargs={'obs_id': image_id})

    def get_initial(self):
        return {
            k: self.request.GET.get(k)
            for k in self.form_class.base_fields.keys()
            if k in self.request.GET
        }


class OngoingExposureView(LoginRequiredMixin, HTMXMixin, TemplateView):
    template_name = 'observation/running/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = ImageSettings.objects.get(pk=self.kwargs['obs_id'])
        return context
