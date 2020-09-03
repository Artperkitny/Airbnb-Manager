from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max

from ...serializer import sync
from ...models import Reservation



class Command(BaseCommand):
    help = 'Sync Reservation DB Table'

    def add_arguments(self, parser):
        parser.add_argument('listing_id', nargs='+', type=int)

    def handle(self, *args, **options):
        last_sync = Reservation.objects.get(Max('last_sync'))
        # sync()

        self.stdout.write(self.style.SUCCESS('"%s"' % last_sync))
