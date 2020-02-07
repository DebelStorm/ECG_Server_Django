# Generated by Django 3.0.2 on 2020-02-07 06:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='File_name',
        ),
        migrations.AddField(
            model_name='data',
            name='File',
            field=models.FileField(default=django.utils.timezone.now, upload_to='~/DJANGO_SERVER_FILES/'),
            preserve_default=False,
        ),
    ]
