# Generated by Django 3.0.2 on 2020-02-04 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patient_number',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]