# Generated by Django 3.0.2 on 2020-03-10 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20200310_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='File',
            field=models.FileField(upload_to='DJANGO_SERVER_FILES/'),
        ),
    ]
