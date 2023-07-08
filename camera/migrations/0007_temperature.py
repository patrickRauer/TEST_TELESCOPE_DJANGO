# Generated by Django 4.1.6 on 2023-07-08 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0006_image_observer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField()),
                ('cooler_on', models.BooleanField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camera.camera')),
            ],
        ),
    ]
