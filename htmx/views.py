from django.shortcuts import render
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.conf import settings
# Create your views here.


class HTMXMixin(TemplateResponseMixin):
    
    def get_template_names(self):
        if not self.request.headers.get('HX-Request', False):
            print('no htmx')
            return settings.BASE_TEMPLATE
        return super().get_template_names()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.headers.get('HX-Request', False):
            context['inner_template'] = self.template_name
        return context
            