from django.contrib import admin

# Register your models here.
from .models import Page, Data


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'date')
    list_filter = ('date',)


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'wind',
        'wind_2m',
        'temperature',
        'temperature_dome',
        'dewpoint',
        'humidity',
        'humidity_dome',
        'rain',
        'date',
    )
    list_filter = ('date',)
