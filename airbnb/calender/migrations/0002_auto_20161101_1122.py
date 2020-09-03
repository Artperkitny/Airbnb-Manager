# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='local_price',
            new_name='airbnb_price',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='status',
            new_name='airbnb_reservation_status',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='reservation_id',
            new_name='nights',
        ),
        migrations.AddField(
            model_name='reservation',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='payout_amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='source',
            field=models.CharField(choices=[('A', 'Airbnb'), ('R', 'Rent')], default=None, max_length=1),
            preserve_default=False,
        ),
    ]