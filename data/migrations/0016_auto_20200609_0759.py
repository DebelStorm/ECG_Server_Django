# Generated by Django 3.0.2 on 2020-06-09 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0015_auto_20200608_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bd_fe',
            name='File',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='data',
            name='File',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='data_filtered',
            name='File',
            field=models.CharField(max_length=300),
        ),
    ]
