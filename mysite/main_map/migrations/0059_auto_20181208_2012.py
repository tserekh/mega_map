# Generated by Django 2.1.1 on 2018-12-08 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_map', '0058_alcostopper_cafe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alcostopper',
            name='cafe',
            field=models.NullBooleanField(),
        ),
    ]
