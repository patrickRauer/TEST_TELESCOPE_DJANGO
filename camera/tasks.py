from django.utils import timezone
from celery import shared_task
from astropy.io import fits
from filter_wheel.models import FilterWheel as FilterWheelDB
from mount.models import Mount
from .models import Camera as CameraDB, Image, ImageSettings, ReadOutTime
import time

from alpaca.camera import Camera
from alpaca.filterwheel import FilterWheel
from alpaca.telescope import Telescope


class ExposureError(Exception):
    ...


@shared_task
def perform_exposures(image_settings_id: int):
    image_settings: ImageSettings = ImageSettings.objects.get(pk=image_settings_id)
    filter_wheel = FilterWheelDB.objects.last()
    filter_wheel = FilterWheel(f'{filter_wheel.ip}:{filter_wheel.port}', filter_wheel.device_id)
    if filter_wheel.Position == -1:
        raise ExposureError(b'Filter wheel moving')

    mount = Mount.objects.last()
    telescope = Telescope(f'{mount.ip}:{mount.port}', mount.device_id)
    if telescope.Slewing:
        raise ExposureError(b'Telescope slewing')

    camera = CameraDB.objects.last()
    camera = Camera(f'{camera.ip}:{camera.port}', camera.device_id)
    if camera.CameraState != 0:
        raise ExposureError(b'Camera is busy')

    filter_wheel.Position = image_settings.filter.position
    while filter_wheel.Position == -1:
        time.sleep(0.1)
    camera.StartX = image_settings.frame.start_x
    camera.StartY = image_settings.frame.start_y
    camera.NumX = image_settings.frame.width
    camera.NumY = image_settings.frame.height
    camera.BinX = image_settings.frame.bin_x
    camera.BinY = image_settings.frame.bin_y

    for i in range(image_settings.repeats):
        camera.StartExposure(
            image_settings.exposure_time,
            image_settings.dark
        )
        image = Image.objects.create(
            exposure_time=image_settings.exposure_time,
            frame=image_settings.frame,
            filter=image_settings.filter,
            dark=image_settings.dark
        )
        while not camera.ImageReady:
            time.sleep(0.5)
        image.finished_at = timezone.now()
        image.save()
        readout_time = time.time()
        image_data = camera.ImageArray
        readout_time = time.time()-readout_time
        ReadOutTime.objects.freate(
            frame=image_settings.frame,
            seconds=readout_time
        )

        fits_file = fits.PrimaryHDU(data=image_data, header=image.to_fits_header())
        path = f'./images/{image.started_at}.fits'
        fits_file.writeto(path)
        image.fits_file = open(path)
