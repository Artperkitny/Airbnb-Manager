# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 01:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_id', models.IntegerField()),
                ('date', models.DateField()),
                ('available', models.BooleanField()),
                ('local_price', models.IntegerField()),
                ('full_name', models.CharField(max_length=100)),
                ('airbnb_user_id', models.IntegerField()),
                ('user_location', models.CharField(max_length=100)),
                ('picture_url', models.URLField()),
                ('status', models.CharField(max_length=100)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.Listing')),
            ],
        ),
    ]
