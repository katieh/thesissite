# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-05 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0029_remove_activity_met_expectation'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='met_expectation',
            field=models.NullBooleanField(default=None),
        ),
    ]
