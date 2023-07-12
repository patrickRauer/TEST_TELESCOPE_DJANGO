from django.views.generic import TemplateView
from datetime import datetime
from htmx.views import HTMXMixin

from .models import CatalogItem
# Create your views here.


class IndexView(HTMXMixin, TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        catalog_items = CatalogItem.objects.all()
        print(self.args)
        context['catalog_items'] = catalog_items
        return context


class CatalogItemView(TemplateView):

    def get_template_names(self):
        return f'catalog/index/{self.request.GET.get("style", "list")}.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogItemView, self).get_context_data(**kwargs)
        catalog_items = CatalogItem.objects.all()
        context['catalog_items'] = catalog_items
        return context
