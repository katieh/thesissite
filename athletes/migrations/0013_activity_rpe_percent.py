# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-03 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0012_auto_20170303_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='RPE_percent',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
