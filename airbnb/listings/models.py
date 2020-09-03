from __future__ import unicode_literals

from django.db import models


class Listing(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    location_unique_name = models.CharField(max_length=30)
    is_airbnb = models.BooleanField(default=True)
    date_created = models.DateTimeField(default='2015-10-01')

    def __str__(self):
        return self.name

