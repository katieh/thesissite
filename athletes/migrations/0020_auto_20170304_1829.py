# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-04 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0019_remove_activity_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='run',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='athletes.Activity'),
        ),
    ]
