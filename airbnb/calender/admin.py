from django.contrib import admin

from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('date', 'listing', 'full_name')

admin.site.register(Reservation, ReservationAdmin)
