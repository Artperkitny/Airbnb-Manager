from django.contrib import admin

from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Listing, ListingAdmin)
