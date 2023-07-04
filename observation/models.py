from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import CatalogItem
from filter_wheel.models import MasterFlat, MasterDark
# Create your models here.


User = get_user_model()


class Observation(models.Model):
    observing_start = models.DateTimeField()
    saved_at = models.DateTimeField(auto_now=True)

    observer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    catalog_item = models.ForeignKey(CatalogItem, on_delete=models.SET_NULL, null=True)

    master_flat = models.ForeignKey(MasterFlat, on_delete=models.SET_NULL, null=True, blank=True)
    master_dark = models.ForeignKey(MasterDark, on_delete=models.SET_NULL, null=True, blank=True)
