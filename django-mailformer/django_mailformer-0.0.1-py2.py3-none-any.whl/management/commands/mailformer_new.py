from django.core.management import BaseCommand

from ...constants import STATUS_
from ...processor import handle_status


class Command(BaseCommand):

    help = "Send emails that are 'NEW', normally this should not occur."

    def handle(self, *args, **options):
        handle_status(status=STATUS_['NEW'])
