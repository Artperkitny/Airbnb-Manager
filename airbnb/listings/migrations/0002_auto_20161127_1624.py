# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 00:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 27, 16, 23, 54, 26429)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='is_airbnb',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='location_unique_name',
            field=models.CharField(default='Palo Alto', max_length=30),
            preserve_default=False,
        ),
    ]