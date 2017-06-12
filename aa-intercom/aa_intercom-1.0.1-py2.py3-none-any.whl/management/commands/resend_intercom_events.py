# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from aa_intercom.models import IntercomEvent
from aa_intercom.tasks import push_intercom_event_task


class Command(BaseCommand):
    help = "Resend intercom events in case something went wrong"

    def handle(self, **options):
        events = IntercomEvent.objects.filter(is_sent=False)
        for e in events:
            push_intercom_event_task.apply_async(args=[e.id], countdown=110)
