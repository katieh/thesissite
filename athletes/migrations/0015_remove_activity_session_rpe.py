# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-03 16:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0014_remove_activity_rpe_percent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='session_RPE',
        ),
    ]