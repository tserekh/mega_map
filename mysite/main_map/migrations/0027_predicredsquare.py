# Generated by Django 2.0.6 on 2018-08-17 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_map', '0026_auto_20180814_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredicredSquare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField(blank=True, null=True)),
                ('y', models.FloatField(blank=True, null=True)),
                ('revenue_pred_model1', models.FloatField(blank=True, null=True)),
                ('revenue_pred_model2', models.FloatField(blank=True, null=True)),
                ('machine_features', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
