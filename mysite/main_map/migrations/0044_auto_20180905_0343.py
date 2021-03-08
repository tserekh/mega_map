# Generated by Django 2.1.1 on 2018-09-05 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_map', '0043_auto_20180905_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groundstop',
            name='lat',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='groundstop',
            name='lon',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='groundstop',
            name='x',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='groundstop',
            name='y',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='lat',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='lon',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='x',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='y',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='metro',
            name='lat',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='metro',
            name='lon',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='metro',
            name='x',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='metro',
            name='y',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='metrostation',
            name='lat',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='metrostation',
            name='lon',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='metrostation',
            name='x',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='metrostation',
            name='y',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='lat',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='lon',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='x',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='y',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='organizationnatclass',
            name='lat',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='organizationnatclass',
            name='lon',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='organizationnatclass',
            name='x',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='organizationnatclass',
            name='y',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='predictedsquare',
            name='x',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='predictedsquare',
            name='y',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='lat',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='lon',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='x',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='y',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
    ]
