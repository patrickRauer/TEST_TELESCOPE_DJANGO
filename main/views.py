from django.views.generic import TemplateView
from htmx.views import HTMXMixin
# Create your views here.


class IndexView(HTMXMixin, TemplateView):
    template_name = 'main/index.html'
