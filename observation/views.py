from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from htmx.views import HTMXMixin

from .forms import ObservationForm


# Create your views here.
class IndexView(HTMXMixin, TemplateView):
    template_name = 'observation/index.html'


class StartExposureFormView(HTMXMixin, FormView):
    template_name = 'observation/exposure/index.html'
    form_class = ObservationForm

    def get_initial(self):
        return {
            k: self.request.GET.get(k)
            for k in self.form_class.base_fields.keys()
            if k in self.request.GET
        }

    def form_valid(self, form):
        response = super().form_valid(form)

        return response
