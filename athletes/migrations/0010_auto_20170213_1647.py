# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-13 16:47
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('athletes', '0009_auto_20170212_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('value', models.PositiveIntegerField(default=1)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='athletes.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='weeks',
            name='weeks',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
