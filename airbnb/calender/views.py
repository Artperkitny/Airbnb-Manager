from collections import OrderedDict
from datetime import timedelta, datetime
from django.http import Http404
from django.http import HttpResponse
from airbnb.listings.models import Listing
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.metadata import BaseMetadata
from rest_framework.response import Response

from .serializer import ReservationSerializer, UpdateReservationSerializer, sync, block_calender
from .models import Reservation


class ReservationView(ListAPIView):
    """
    Returns Reservation data in JSON format.
    Accepts the following GET parameters: token
    """
    # permission_classes = (IsAuthenticated,)

    serializer_class = ReservationSerializer
    model = serializer_class.Meta.model

    def get_queryset(self, **kwargs):
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        listing = self.kwargs['listing']
        reservation_object = self.model.objects.filter(date__range=[start_date, end_date], listing__id=listing).order_by('date')
        return reservation_object


class UpdateReservationView(UpdateAPIView):
    """
    Returns Reservation data in JSON format.

    """
    serializer_class = UpdateReservationSerializer

    def get_object(self):
        date = self.kwargs['date']
        listing = self.kwargs['listing']
        listing_instance = Listing.objects.get(id=listing)

        if listing_instance.is_airbnb:
            if self.request.data['source'] is not 'Airbnb' and self.request.data['available'] == False:

                start_date = self.request.data['start_date']
                end_date = datetime.strftime(datetime.strptime(start_date,"%Y-%m-%d") + timedelta(days=int(self.request.data['nights'])-1), '%Y-%m-%d')

                # Check to make sure no one has booked during the runtime of this script
                if datetime.strptime(date, '%Y-%m-%d') == datetime.strptime(start_date, '%Y-%m-%d'):
                    sync(start_date, end_date, [listing, ])
                    block_calender(listing, start_date, end_date, 'unavailable', self.request.data['full_name'])

                reservation_object = Reservation.objects.get(date=date, listing__id=listing)

            elif self.request.data['source'] is not 'Airbnb':
                reservation_object = Reservation.objects.get(date=date, listing__id=listing)
                start_date = self.request.data['start_date']
                end_date = datetime.strftime(datetime.strptime(start_date,"%Y-%m-%d") + timedelta(days=int(self.request.data['nights'])), '%Y-%m-%d')
                if datetime.strptime(date, '%Y-%m-%d') == datetime.strptime(start_date, '%Y-%m-%d'):
                    block_calender(listing, start_date, end_date, 'available')
            else:
                reservation_object = Reservation.objects.get(date=date, listing__id=listing)

        else:
            reservation_object = Reservation.objects.get(date=date, listing__id=listing)

        return reservation_object
