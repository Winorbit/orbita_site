# Generated by Django 3.0.6 on 2020-05-29 11:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_app', '0005_auto_20200529_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_courses',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=36), default=[], size=None),
        ),
    ]
