from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^reservation/(?P<listing>.+)/(?P<start_date>.+)/(?P<end_date>.+)/', views.ReservationView.as_view(), name='reservation'),
    url(r'^update_reservation/(?P<listing>.+)/(?P<date>.+)/', views.UpdateReservationView.as_view(), name='reservation'),
]
