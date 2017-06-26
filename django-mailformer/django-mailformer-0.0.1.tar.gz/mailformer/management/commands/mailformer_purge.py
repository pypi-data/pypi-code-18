from datetime import timedelta

from django.core.management import BaseCommand
from django.utils.timezone import now

from ...constants import STATUS_
from ...models import Message


class Command(BaseCommand):

    help = "Delete send mails older than 1 day (by default)."

    def add_arguments(self, parser):
        parser.add_argument('--older_than_days', default=1, type=int)

    def handle(self, *args, **options):
        delta = timedelta(days=options['older_than_days'])

        age = now() - delta

        query_kwargs = {
            'status': STATUS_['SENT'],
            'updated_at__lte': age,
        }

        Message.objects.filter(**query_kwargs).delete()
