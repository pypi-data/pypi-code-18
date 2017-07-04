"""This module will contain the utilities we will use for the tests"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from affiliations.models import Partner


@receiver(post_save)
def partner_updated(sender, instance, affiliate_trigger_name=None, **kwargs):
    """

    :param sender:
    :param instance:
    :param affiliate_trigger_name:
    :return:
    """
    if isinstance(instance, Partner):
        Partner.objects.filter(pk=instance.pk).update(active=True)
