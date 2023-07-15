from logging import getLogger

from celery import shared_task
from .utils import TcpDome
from .models import Dome

from mount.models import Mount
from alpaca.telescope import Telescope


log = getLogger(__name__)


def _get_dome():
    mount = Mount.objects.last()
    mount = Telescope(f'{mount.ip}:{mount.port}', mount.device_id)
    return TcpDome(mount)


def dome_decorator(func):

    def inject_dome(*args, **kwargs):
        kwargs['dome'] = _get_dome()
        return func(*args, **kwargs)
    return inject_dome


@shared_task
@dome_decorator
def move_to_azimuth(azimuth: float, dome: TcpDome = None):
    dome.slew_dome(azimuth)


@shared_task
@dome_decorator
def open_shutter(dome: TcpDome = None):
    dome.open_shutter()


@shared_task
@dome_decorator
def close_shutter(dome: TcpDome = None):
    dome.close_shutter()


@shared_task
@dome_decorator
def align_dome_mount(dome: TcpDome = None):
    """
    Moves the dome actively, if it exceeds the limit
    """
    if dome.mount.Tracking:
        dome = Dome.objects.last()

        # if auto alignment is deactivated, do nothing
        if not dome.auto_alignment:
            return

        mount_azimuth = dome.mount.Azimuth
        dome_azimuth = dome.get_az()
        delta_azimuth = abs(mount_azimuth-dome_azimuth)

        # if they are over the limit, move the dome
        if delta_azimuth > dome.azimuth_limit:
            dome.slew_dome(mount_azimuth)
            log.info('Dome and mount azimuth are above the limit, move dome.')
