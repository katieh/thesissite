# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-27 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0003_activity_elevation_gained'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='comments',
            field=models.TextField(default=None, null=True),
        ),
    ]