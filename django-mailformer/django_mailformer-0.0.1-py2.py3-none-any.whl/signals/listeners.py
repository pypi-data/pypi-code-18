from django.db.models.signals import post_save
from django.dispatch import receiver

from .. import processor
from ..constants import STATUS_
from ..models import Message


@receiver(post_save, sender=Message)
def process_atomic(sender, instance, raw, **kwargs):
    "Atomic Message process filter."
    if raw:
        return

    if instance.status in (STATUS_['NEW'], STATUS_['RETRY']):
        processor.handle_status(instance.status, instance.id)
