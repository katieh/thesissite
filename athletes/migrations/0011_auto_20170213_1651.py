# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-13 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0010_auto_20170213_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='value',
            field=models.FloatField(default=1),
        ),
    ]
