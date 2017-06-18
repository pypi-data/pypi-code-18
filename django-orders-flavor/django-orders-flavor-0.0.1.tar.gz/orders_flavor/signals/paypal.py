import logging

from django.conf import settings
from django.dispatch import receiver

from paypal.standard.ipn import signals as ipn_signals
from paypal.standard.models import ST_PP_COMPLETED

from .. import models


logger = logging.getLogger(__name__)


@receiver(ipn_signals.valid_ipn_received)
def paypal_ipn_verify(sender, **kwargs):
    paypal_ipn = sender

    if paypal_ipn.receiver_email == settings.PAYPAL_BUSINESS:
        try:
            order = models.Order.objects.get(id=paypal_ipn.custom)
        except models.Order.DoesNotExist:
            return

        # check the amount received etc. are all what you expect.
        if paypal_ipn.payment_status != ST_PP_COMPLETED:
            order.satus = models.Order.CANCELLED

        elif (order.status == models.Order.PENDING and
              order.amount == paypal_ipn.amount):

            order.satus = models.Order.PAID
        else:
            order.satus = models.Order.DENIED

        order.payment_method = paypal_ipn
        order.save()


@receiver(ipn_signals.invalid_ipn_received)
def notify_invalid_ipn(sender, **kwargs):
    logger.error('Invalid ipn received', {'id': sender.id})
