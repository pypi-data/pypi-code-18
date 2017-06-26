from django.core.management import BaseCommand

from ...constants import STATUS_
from ...processor import handle_status


class Command(BaseCommand):

    help = "Retry sending emails that have been marked as 'RETRY'."

    def handle(self, *args, **options):
        handle_status(status=STATUS_['RETRY'])
