# Generated by Django 3.0.2 on 2020-02-03 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firmware', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmware_version',
            name='Firmware_Version_id',
            field=models.CharField(blank=True, default=' N/A ', max_length=100),
        ),
        migrations.AlterField(
            model_name='firmware_version',
            name='Firmware_version_number',
            field=models.CharField(blank=True, default=' N/A ', max_length=100),
        ),
    ]