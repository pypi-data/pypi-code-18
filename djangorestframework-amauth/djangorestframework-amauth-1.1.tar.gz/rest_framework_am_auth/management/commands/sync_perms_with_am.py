# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from rest_framework_am_auth.account_manager_client import AccountManagerClient


class Command(BaseCommand):
    help = 'Synchronises permissions with Account Manager'

    def handle(self, *args, **options):
        client = AccountManagerClient()
        self.stdout.write(
            u'%s' % client.synchronize_permissions()
        )
