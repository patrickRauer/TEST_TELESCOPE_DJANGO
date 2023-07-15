from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from htmx.views import HTMXMixin
from .tasks import _get_dome
from .forms import MoveDomeForm, AutoAlignmentForm, SwitchShutterForm
from .models import Dome
# Create your views here.


class IndexView(LoginRequiredMixin, HTMXMixin, TemplateView):
    """
    Main dome view
    """
    template_name = 'dome/index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dome = _get_dome()
        context['shutter'] = {
            'status': dome.get_shutter_status()
        }
        context['move_dome_form'] = MoveDomeForm()
        dome = Dome.objects.last()
        context['auto_alignment_form'] = AutoAlignmentForm(
            initial={'activate': dome.auto_alignment}
        )
        return context


class OpenCloseShutterFormView(LoginRequiredMixin, FormView):
    """
    FormView to open and close the shutter of the dome
    No template rendering!!!
    """
    template_name = ''
    form_class = SwitchShutterForm

    def form_valid(self, form):
        dome = _get_dome()
        shutter_status = dome.get_shutter_status()
        if shutter_status == 'open':
            dome.close_shutter()
        elif shutter_status == 'closed':
            dome.open_shutter()
        else:
            return HttpResponse(status=400)
        return HttpResponse(status=201)


class AutoAlignmentFormView(LoginRequiredMixin, FormView):
    """
    FormView to activate and deactivate the auto alignment
    No template rendering!!!
    """
    template_name = ''
    form_class = AutoAlignmentForm

    def form_valid(self, form):
        dome = Dome.objects.last()
        dome.auto_alignment = 'activate' in form.data
        dome.save()
        return HttpResponse(status=201)


class MoveDomeFormView(LoginRequiredMixin, FormView):
    """
    FormView to receive commands to move the dome
    No template rendering!!!
    """
    template_name = ''
    form_class = MoveDomeForm

    def form_valid(self, form):
        dome = _get_dome()
        dome.slew_dome(form.data['azimuth'])
        return HttpResponse(status=201)
