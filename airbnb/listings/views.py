import requests
import json

from rest_framework.generics import ListAPIView

from airbnb.globals import *
from .models import Listing
from .serializer import ListingSerializer


def get_airbnb_listings(_offset=0, _limit=10, number_of_listings=0, listings=[]):
    has_availability = 'false'
    _format = 'v1_legacy_long'
    url = "https://api.airbnb.com/v2/listings?user_id={0}&has_availability={1}&_offset={2}&_limit={3}&_format={4}&currency={5}&locale={6}&client_id={7}".format(USER_ID, has_availability, _offset, _limit, _format, CURRENCY, LOCALE, CLIENT_ID)

    response = requests.get(url)
    json_response = response.json()

    for listing in json_response['listings']:
        listings.append(listing)

    if number_of_listings==0:
        number_of_listings = json_response['metadata']['listing_count']-_offset

    if number_of_listings > 10 and number_of_listings <= 20:
        listings.append(get_airbnb_listings(_offset=_offset+10, _limit=(number_of_listings-10), number_of_listings=number_of_listings-10))

    elif number_of_listings > 20:
        listings.append(get_airbnb_listings(_offset=_offset+10, _limit=10, number_of_listings=number_of_listings-10))

    return listings


def init():
    print "Syncing Airbnb Listings"
    listings = get_airbnb_listings()
    for listing in listings:
        Listing.objects.get_or_create(id=listing['id'], name=listing['name'])


def update():
    pass


class ListingView(ListAPIView):
    """
    Returns Listing data in JSON format.
    Accepts the following GET parameters: token
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = ListingSerializer
    # model = serializer_class.Meta.model

    def get_queryset(self):
        listing_object = Listing.objects.all().order_by('name')
        return listing_object
