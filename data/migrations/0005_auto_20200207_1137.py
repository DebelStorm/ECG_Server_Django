# Generated by Django 3.0.2 on 2020-02-07 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_data_data_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='File',
            field=models.FileField(upload_to='DJANGO_SERVER_FILES/'),
        ),
    ]
