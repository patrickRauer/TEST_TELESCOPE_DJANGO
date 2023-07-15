from django.apps import AppConfig


def _create_default_tasks():
    from django_celery_beat.models import IntervalSchedule, PeriodicTask
    every_minutes = IntervalSchedule.objects.get_or_create(every=1, period='minutes')
    PeriodicTask.objects.get_or_create(
        name='Align mount and dome',
        description='Aligns the mount and the dome by checking the difference of the azimuth and '
                    'if it exceeds the limit, moves the dome.',
        task='dome.tasks.align_dome_mount',
        interval=every_minutes
    )


class DomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dome'
