from django.contrib import admin

from .models import Mount, Coordinate


@admin.register(Mount)
class MountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip', 'device_id')
    search_fields = ('name',)


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ('id', 'ra', 'dec', 'date')
    list_filter = ('date',)
