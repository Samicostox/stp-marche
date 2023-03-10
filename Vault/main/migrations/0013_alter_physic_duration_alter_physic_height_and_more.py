# Generated by Django 4.0.6 on 2023-01-23 13:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_user_isnexuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physic',
            name='duration',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='physic',
            name='height',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=20), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='physic',
            name='weight',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=20), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='physic',
            name='weight_goal',
            field=models.IntegerField(),
        ),
    ]
