# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-03 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0011_auto_20170213_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='RPE',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='session_RPE',
            field=models.PositiveIntegerField(null=True),
        ),
    ]