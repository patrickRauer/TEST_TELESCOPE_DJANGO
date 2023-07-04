from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from htmx.views import HTMXMixin

from .models import FilterWheel

from alpaca.filterwheel import FilterWheel
# Create your views here.


class ChangeFilterFormView(LoginRequiredMixin, HTMXMixin, FormView):
    template_name = ''
    form_class = None

    def get_success_url(self):
        return ''

    def form_valid(self, form):
        clean_data = form.clean_data
        filter_wheel = clean_data['filter'].filter_wheel
        filter_wheel: FilterWheel = FilterWheel(filter_wheel.ip, filter_wheel.device_number)
        filter_wheel.Position = clean_data['filter'].position
        return HttpResponse(status=201)
