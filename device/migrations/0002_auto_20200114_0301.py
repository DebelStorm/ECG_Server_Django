# Generated by Django 3.0.2 on 2020-01-14 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='serial_number',
            field=models.CharField(blank=True, default='00000000000000', max_length=100),
        ),
    ]
