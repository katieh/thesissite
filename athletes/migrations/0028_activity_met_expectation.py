# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-05 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0027_tag_allow_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='met_expectation',
            field=models.BooleanField(default=False),
        ),
    ]
