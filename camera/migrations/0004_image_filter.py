# Generated by Django 4.1.6 on 2023-07-07 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filter_wheel', '0002_filterwheel_port_alter_filterwheel_device_id_and_more'),
        ('camera', '0003_frame_readouttime_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='filter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='filter_wheel.filter'),
        ),
    ]