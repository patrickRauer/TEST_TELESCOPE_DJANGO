# Generated by Django 4.1.6 on 2023-07-02 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('ip', models.GenericIPAddressField()),
                ('device_id', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]