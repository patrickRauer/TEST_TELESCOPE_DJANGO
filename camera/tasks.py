from django.utils import timezone
from os import environ
from pathlib import Path
from astropy.io import fits
from filter_wheel.models import FilterWheel as FilterWheelDB
from mount.models import Mount
from .models import Camera as CameraDB, Image, ImageSettings, ReadOutTime, Temperature
import time

from alpaca.camera import Camera
from alpaca.filterwheel import FilterWheel
from alpaca.telescope import Telescope
"""if 'REDIS_URL' in environ:
    from celery import shared_task
else:
    from threading import Thread


    class AsyncTask(Thread):
        args = None
        kwargs = None

        def __init__(self, func):
            super().__init__()
            self.func = func

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        def run(self) -> None:
            self.func(*self.args, **self.kwargs)

        def delay(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self.start()

    def shared_task(func):

        return AsyncTask(func)

"""
from celery import shared_task
class ExposureError(Exception):
    ...


def _get_devices() -> tuple[FilterWheel, Camera]:
    """
    Takes the latest entry for the camera :class:`CameraDB` and filter wheel (:class:`FilterWheelDB`) from
    the database and creates alpaca/alpyca :class:`Camera' and :class:`FilterWheel` objects out of it.
    """
    filter_wheel = FilterWheelDB.objects.last()
    filter_wheel = FilterWheel(f'{filter_wheel.ip}:{filter_wheel.port}', filter_wheel.device_id)
    camera = CameraDB.objects.last()
    camera = Camera(f'{camera.ip}:{camera.port}', camera.device_id)
    return filter_wheel, camera


def _check_devices(filter_wheel: FilterWheel, camera: Camera):
    """
    Checks if the filter wheel, the camera and the mount are ready for an exposure.

    :raise ExposureError: If one of the devices is not ready.
    """
    if filter_wheel.Position == -1:
        raise ExposureError(b'Filter wheel moving')

    mount = Mount.objects.last()
    telescope = Telescope(f'{mount.ip}:{mount.port}', mount.device_id)
    if telescope.Slewing:
        raise ExposureError(b'Telescope slewing')

    if camera.CameraState != 0:
        raise ExposureError(b'Camera is busy')


def _apply_image_settings(image_settings: ImageSettings, filter_wheel: FilterWheel, camera: Camera):
    """
    Move the filter wheel in the right position and applies the image frame settings (size and binning).
    """
    filter_wheel.Position = image_settings.filter.position
    while filter_wheel.Position == -1:
        time.sleep(0.1)
    camera.StartX = image_settings.frame.start_x
    camera.StartY = image_settings.frame.start_y
    camera.NumX = image_settings.frame.width
    camera.NumY = image_settings.frame.height
    camera.BinX = image_settings.frame.bin_x
    camera.BinY = image_settings.frame.bin_y


def _take_image(image_settings: ImageSettings, camera: Camera):
    camera.StartExposure(
        image_settings.exposure_time,
        image_settings.dark
    )
    image = Image.objects.create(
        exposure_time=image_settings.exposure_time,
        frame=image_settings.frame,
        filter=image_settings.filter,
        dark=image_settings.dark,
        observer=image_settings.observer
    )
    while not camera.ImageReady:
        time.sleep(0.5)
    image.finished_at = timezone.now()
    image.save()
    readout_time = time.time()
    image_data = camera.ImageArray
    readout_time = time.time() - readout_time
    ReadOutTime.objects.create(
        frame=image_settings.frame,
        seconds=readout_time
    )

    header = fits.Header(image.to_fits_header())
    fits_file = fits.PrimaryHDU(data=image_data, header=header)
    path = Path(f'./images/{image.started_at}.fits')
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    fits_file.writeto(path)
    image.fits_file.name = str(path.as_posix())
    image.save()


@shared_task
def perform_exposures(image_settings_id: int):
    """
    Applies the image settings and starts the actual exposure

    :raise ExposureError: If the telescope is slewing, if the filter wheel is rotating or if the camera is busy.
    """
    image_settings: ImageSettings = ImageSettings.objects.get(pk=image_settings_id)
    filter_wheel, camera = _get_devices()

    _check_devices(filter_wheel, camera)
    _apply_image_settings(image_settings, filter_wheel, camera)

    for i in range(image_settings.repeats):
        _take_image(image_settings, camera)


@shared_task
def track_camera_temperature():
    """
    Reads CCD temperature of the camera and if the cooler of the camera is on and
    stores the data into the database.
    """
    filter_wheel, camera = _get_devices()
    temperature = camera.CCDTemperature
    cooler_on = camera.CoolerOn

    Temperature.objects.create(
        temperature=temperature,
        cooler_on=cooler_on,
        camera=CameraDB.objects.last()
    )
