# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0008_auto_20161103_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='car',
            field=models.NullBooleanField(default=None),
        ),
    ]
