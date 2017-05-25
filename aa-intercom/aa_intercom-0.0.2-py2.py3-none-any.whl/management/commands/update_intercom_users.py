from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

import time


class Command(BaseCommand):
    help = "Update all users in intercom.io"

    def handle(self, **options):
        # return  # not sure if it is not needed. Commenting out for now to check.
        for u in get_user_model().objects.all():
            time.sleep(0.5)  # because of the limit on intercom
            u.save()
