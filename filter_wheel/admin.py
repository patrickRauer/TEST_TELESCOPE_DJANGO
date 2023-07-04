from django.contrib import admin

from .models import FilterWheel, Filter, DarkImage, MasterDark, FlatImage, MasterFlat


@admin.register(FilterWheel)
class FilterWheelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip', 'device_id')
    search_fields = ('name',)


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'filter_wheel',
        'name',
        'letter',
        'position',
        'flat_time',
    )
    list_filter = ('filter_wheel',)
    search_fields = ('name',)


@admin.register(DarkImage)
class DarkImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'observing_time')


@admin.register(MasterDark)
class MasterDarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'observing_time')
    raw_id_fields = ('darks',)


@admin.register(FlatImage)
class FlatImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'filter', 'master_dark', 'created_at')
    list_filter = ('filter', 'master_dark', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(MasterFlat)
class MasterFlatAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('flats',)
    date_hierarchy = 'created_at'
