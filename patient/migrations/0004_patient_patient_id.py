# Generated by Django 3.0.2 on 2020-02-07 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20200204_0603'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
