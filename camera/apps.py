from django.apps import AppConfig


def _create_default_periodic_tasks():
    from django_celery_beat.models import PeriodicTask, IntervalSchedule

    interval, _ = IntervalSchedule.objects.get_or_create(
        period='minutes',
        every=1
    )
    PeriodicTask.objects.get_or_create(
        name='Track camera temperature',
        interval=interval,
        task='camera.tasks.track_camera_temperature',
        description='Reads the temperature of the camera and save the value to the database'
    )


def _create_dummy_camera_entry():
    from camera.models import Camera

    if not Camera.objects.all().exists():
        Camera.objects.create(
            name='Camera',
            ip='192.168.2.100',
            port=32323,
            device_id=0
        )


class CameraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'camera'

    def ready(self):
        _create_dummy_camera_entry()
        _create_default_periodic_tasks()
        from camera import tasks
