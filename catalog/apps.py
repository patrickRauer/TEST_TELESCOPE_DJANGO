from django.apps import AppConfig


def _create_default_entries():
    from catalog.models import Type

    for n in ['Exo-planet', 'Binary', 'QSO']:
        Type.objects.get_or_create(name=n)


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        _create_default_entries()
