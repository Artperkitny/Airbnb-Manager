from __future__ import unicode_literals

from django.db import models
from airbnb.listings.models import Listing


class Reservation(models.Model):
    AIRBNB = "Airbnb"
    RENT = "Rent"
    WEBSITE = "Website"

    SOURCE_CHOICES = (
        (AIRBNB, 'Airbnb'),
        (RENT, 'Rent'),
        (WEBSITE, 'Website'),
    )

    listing = models.ForeignKey(Listing)
    date = models.DateField(blank=False)

    available = models.BooleanField(default=True)
    full_name = models.CharField(null=True, max_length=100)
    source = models.CharField(max_length=9, choices=SOURCE_CHOICES, null=True)
    paid_amount = models.FloatField(null=True)
    payout_amount = models.FloatField(null=True)
    payment_status = models.NullBooleanField()
    nights = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_sync = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=1000, null=True)
    start_date = models.DateField(null=True)

    # Airbnb Reservation Specific Fields
    airbnb_user_id = models.IntegerField(null=True)
    airbnb_reservation_status = models.CharField(null=True, max_length=100)
    airbnb_price = models.IntegerField(null=True)

    airbnb_confirmation_code = models.CharField(null=True, max_length=9)
    airbnb_number_of_guests = models.IntegerField(null=True)
    airbnb_guest_checkin_at = models.DateTimeField(null=True)
    airbnb_thread_id = models.IntegerField(null=True)
    airbnb_type = models.CharField(null=True, max_length=100)
    airbnb_group_id = models.CharField(null=True, max_length=100)

    # Superlatives
    user_location = models.CharField(null=True, max_length=100)
    picture_url = models.URLField(null=True)
    has_car = models.NullBooleanField(default=None)

    # Check-in Time
    # Checkout Time
    # Airbnb_review

