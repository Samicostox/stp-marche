# Generated by Django 4.0.6 on 2023-01-23 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_user_recomeal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isnexuser',
            field=models.BooleanField(default=False),
        ),
    ]
