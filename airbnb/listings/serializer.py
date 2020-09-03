from rest_framework import serializers

from airbnb.listings.models import Listing


class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing

        fields = (
            'id',
            'name',

        )

        read_only_fields = [
            'id',
            'name',
        ]


