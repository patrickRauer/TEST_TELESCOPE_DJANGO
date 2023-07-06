from django.apps import AppConfig


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
