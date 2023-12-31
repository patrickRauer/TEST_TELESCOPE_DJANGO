# Generated by Django 4.1.6 on 2023-07-03 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mount', '0002_mount'),
    ]

    operations = [
        migrations.AddField(
            model_name='mount',
            name='port',
            field=models.PositiveSmallIntegerField(default=32323, help_text='Used port of the device'),
        ),
        migrations.AlterField(
            model_name='mount',
            name='device_id',
            field=models.PositiveSmallIntegerField(help_text='Device ID of the device'),
        ),
        migrations.AlterField(
            model_name='mount',
            name='ip',
            field=models.GenericIPAddressField(help_text='Static IP of the device'),
        ),
        migrations.AlterField(
            model_name='mount',
            name='name',
            field=models.CharField(help_text='Name of the device', max_length=40),
        ),
    ]
