from django.contrib import admin

from .models import Camera, Temperature, Frame, ReadOutTime, Image, ImageSettings


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip', 'port', 'device_id')
    search_fields = ('name',)


@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'temperature', 'cooler_on', 'date', 'camera')
    list_filter = ('cooler_on', 'date', 'camera')


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'start_x',
        'start_y',
        'width',
        'height',
        'bin_x',
        'bin_y',
    )


@admin.register(ReadOutTime)
class ReadOutTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'frame', 'seconds', 'date')
    list_filter = ('frame', 'date')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'frame',
        'exposure_time',
        'filter',
        'dark',
        'observer',
        'started_at',
        'finished_at',
        'fits_file',
    )
    list_filter = (
        'frame',
        'filter',
        'dark',
        'observer',
        'started_at',
        'finished_at',
    )


@admin.register(ImageSettings)
class ImageSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'frame',
        'exposure_time',
        'filter',
        'dark',
        'observer',
        'started_at',
        'finished_at',
        'repeats',
        'images_done',
    )
    list_filter = (
        'frame',
        'filter',
        'dark',
        'observer',
        'started_at',
        'finished_at',
    )
