# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-10 04:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0023_auto_20170307_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='avg_speed',
        ),
    ]
