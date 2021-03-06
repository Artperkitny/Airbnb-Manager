# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0002_auto_20161101_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='airbnb_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='airbnb_reservation_status',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='airbnb_user_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='nights',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payout_amount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='picture_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user_location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
