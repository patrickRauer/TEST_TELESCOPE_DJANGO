from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from htmx.views import HTMXMixin
# Create your views here.


class IndexView(LoginRequiredMixin, HTMXMixin, TemplateView):
    template_name = ''
