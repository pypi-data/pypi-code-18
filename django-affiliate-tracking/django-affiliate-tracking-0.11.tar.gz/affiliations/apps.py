"""Configuration of the application affiliations."""

from __future__ import unicode_literals

from functools import partial

from django.apps import AppConfig
from django.conf import settings

from .utils import import_from_path


class AffiliateTrackingConfig(AppConfig):
    """Class representing the affiliations Django application."""

    name = 'affiliations'

    def ready(self):
        """Connect the signals from AFFILIATE_TRIGGERS."""
        for (
                name,
                signal_path,
                receiver_path,
                sender_path
        ) in settings.AFFILIATE_TRIGGERS:
            signal = import_from_path(signal_path)
            receiver = import_from_path(receiver_path)
            sender = import_from_path(sender_path)
            signal.connect(
                partial(
                    receiver,
                    affiliate_trigger_name=name
                ),
                sender=sender,
                weak=False
            )
