import requests
import datetime
from datetime import timedelta
from rest_framework import serializers

from .models import Reservation
from airbnb.globals import *
from airbnb.listings.models import Listing


URL = "https://api.airbnb.com/v2/batch/?client_id={0}&currency={1}&locale={2}".format(CLIENT_ID, CURRENCY, LOCALE)


def fetch_calender(start_date, end_date, listing_id):
    headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Airbnb-OAuth-Token': ACCESS_TOKEN}
    parameters = {"operations": [{"method": "GET", "path": "/calendar_days",
                                  "query": {"start_date": "{0}".format(start_date), "listing_id": "{0}".format(listing_id),
                                            "_format": "host_calendar", "end_date": "{0}".format(end_date)}},
                                 {"method": "GET", "path": "/dynamic_pricing_controls/12132179", "query": {}}],
                  "_transaction": False}
    return requests.post(URL, headers=headers, json=parameters)


def init(start_date, end_date):
    listings = Listing.objects.all()
    datetime_interval = (datetime.datetime.strptime(end_date,'%Y-%m-%d') - datetime.datetime.strptime(start_date,'%Y-%m-%d')).days + 1
    for listing in listings:
        for i in range(datetime_interval):
            print "updating {0} {1}".format(listing, datetime.datetime.strptime(start_date, '%Y-%m-%d')+timedelta(i))
            Reservation.objects.get_or_create(date=datetime.datetime.strptime(start_date, '%Y-%m-%d')+timedelta(i), listing=listing)


def process(data, listing):
    data_list = []
    data_json = data.json()
    for day in data_json['operations'][0]['response']['calendar_days']:
        try:
            previous_reservation_object = Reservation.objects.get(date=day['date'], listing=listing)
        except Reservation.DoesNotExist:
            previous_reservation_object['reservation'] = None
        data = dict()
        data['listing'] = listing
        data['date'] = day['date']
        data['available'] = day['available']
        data['airbnb_price'] = day['price']['local_price'] # Current Airbnb Price

        # Reservation was canceled via Airbnb
        if previous_reservation_object.airbnb_reservation_status is not None and data['available'] == True:
            data['airbnb_reservation_status'] = None
            data['full_name'] = None
            data['airbnb_user_id'] = None
            data['picture_url'] = None
            data['user_location'] = None
            data['payout_amount'] = None
            data['nights'] = None
            data['source'] = None
            data['airbnb_confirmation_code'] = None
            data['airbnb_number_of_guests'] = None
            data['airbnb_guest_checkin_at'] = None
            data['start_date'] = None
            data['airbnb_thread_id'] = None
            data['airbnb_type'] = None
            data['airbnb_group_id'] = None
            data['payment_status'] = None
            data['paid_amount'] = None

        # Do this if there exists an Airbnb reservation for this listing on this date
        if day['reservation'] is not None:
            data['airbnb_reservation_status'] = day['reservation']['status']
            data['full_name'] = day['reservation']['guest']['full_name']
            data['airbnb_user_id'] = day['reservation']['guest']['id']
            data['picture_url'] = day['reservation']['guest']['picture_url']
            data['user_location'] = day['reservation']['guest']['location']
            data['payout_amount'] = day['reservation']['localized_payout_price'] # Amount Paid to Host for Reservation
            data['nights'] = day['reservation']['nights']
            data['source'] = 'Airbnb'
            data['airbnb_confirmation_code'] = day['reservation']['confirmation_code']
            data['airbnb_number_of_guests'] = day['reservation']['number_of_guests']
            data['airbnb_guest_checkin_at'] = day['reservation']['guest_checkin_at']
            data['start_date'] = day['reservation']['start_date']
            data['airbnb_thread_id'] = day['reservation']['thread_id']
            data['airbnb_type'] = day['type']
            data['airbnb_group_id'] = day['group_id']
            data['payment_status'] = True
            data['paid_amount'] = day['reservation']['localized_payout_price']

        data_list.append(data)

    update(data_list)


def update(data):
    for day in data:
        print day['listing'], day['date'], '\n'
        day['listing'] = Listing.objects.get(id=day['listing'])
        obj, created = Reservation.objects.update_or_create(date=day['date'], listing=day['listing'], defaults=day)


def sync(start_date, end_date, listings=Listing.objects.all().exclude(is_airbnb=False).values_list('id', flat=True)):
    for listing in listings:
        process(fetch_calender(start_date, end_date, listing), listing)


def block_calender(listing_id, start_date, end_date, availability, notes=""):
    url = "https://api.airbnb.com/v2/calendars/{0}/{1}/{2}?client_id={3}&currency={4}&locale={5}".format(listing_id, start_date, end_date, CLIENT_ID, CURRENCY, LOCALE)
    headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Airbnb-OAuth-Token' : ACCESS_TOKEN}
    parameters = {"availability":"{}".format(availability), "notes":"{}".format(notes)}
    response = requests.put(url, headers = headers, json=parameters)
    if response.status_code == 200:
        return 'set availability to: {0} and note to: {1} for {2} to {3} \n'.format(availability, notes, start_date, end_date)
    else:
        return 'Failed to block or un-block Airbnb dates for {0} to {1} \n'.format(start_date, end_date)


def sync_non_airbnb_listing_dates(listings=Listing.objects.all().exclude(is_airbnb=True).values_list('id', flat=True)):
    start_date = Reservation.objects.earliest('date').date
    end_date = Reservation.objects.latest('date').date
    day_count = (end_date - start_date).days + 1
    for listing in listings:
        for date in (start_date + timedelta(n) for n in range(day_count)):
            Reservation.objects.get_or_create(listing_id=listing, date=date, available=True)


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = (
                    "listing_id",
                    "date",
                    "available",
                    "full_name",
                    "source",
                    "payout_amount",
                    "payment_status",
                    "nights",
                    "created",
                    "last_sync",
                    "notes",
                    "airbnb_user_id",
                    "airbnb_reservation_status",
                    "airbnb_price",
                    "airbnb_confirmation_code",
                    "airbnb_number_of_guests",
                    "airbnb_guest_checkin_at",
                    "airbnb_thread_id",
                    "airbnb_type",
                    "airbnb_group_id",
                    "user_location",
                    "picture_url",
                    "has_car",
                    "start_date",
                    "paid_amount",
        )


class UpdateReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = (
                    "listing_id",
                    "date",
                    "available",
                    "full_name",
                    "source",
                    "payout_amount",
                    "payment_status",
                    "nights",
                    "created",
                    "last_sync",
                    "notes",
                    "airbnb_user_id",
                    "airbnb_reservation_status",
                    "airbnb_price",
                    "airbnb_confirmation_code",
                    "airbnb_number_of_guests",
                    "airbnb_guest_checkin_at",
                    "airbnb_thread_id",
                    "airbnb_type",
                    "airbnb_group_id",
                    "user_location",
                    "picture_url",
                    "has_car",
                    "start_date",
                    "paid_amount",
        )

        read_only_fields = [
                    "listing_id",
                    "date",
                    "airbnb_user_id",
                    "airbnb_reservation_status",
                    "airbnb_price",
                    "airbnb_confirmation_code",
                    "airbnb_number_of_guests",
                    "airbnb_guest_checkin_at",
                    "airbnb_thread_id",
                    "airbnb_type",
                    "airbnb_group_id",
                    "created",
                    "last_sync",
        ]

    def update(self, instance, validated_data):

        if instance.source != 'Airbnb':

            instance.source = validated_data.get('source', instance.source)
            instance.available = validated_data.get('available', instance.available)

            if instance.available is not True:
                instance.full_name = validated_data.get('full_name', instance.full_name)
                instance.payout_amount = validated_data.get('payout_amount', instance.payout_amount)
                instance.payment_status = validated_data.get('payment_status', instance.payment_status)
                instance.nights = validated_data.get('nights', instance.nights)
                instance.user_location = validated_data.get('user_location', instance.user_location)
                instance.picture_url = validated_data.get('picture_url', instance.picture_url)
                instance.notes = validated_data.get('notes', instance.notes)
                instance.has_car = validated_data.get('has_car', instance.has_car)
                instance.start_date = validated_data.get('start_date', instance.start_date)
                instance.paid_amount = validated_data.get('paid_amount', instance.paid_amount)

            else:
                instance.full_name = None
                instance.picture_url = None
                instance.user_location = None
                instance.payout_amount = None
                instance.nights = None
                instance.source = None
                instance.start_date = None
                instance.payment_status = None
                instance.notes = None
                instance.has_car = None
                instance.paid_amount = None

        else:
            instance.notes = validated_data.get('notes', instance.notes)
            instance.has_car = validated_data.get('has_car', instance.has_car)

        instance.save()

        return instance
