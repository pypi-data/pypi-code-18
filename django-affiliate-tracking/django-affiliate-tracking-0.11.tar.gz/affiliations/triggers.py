"""Built in trigger receivers for the most common cases."""

from __future__ import unicode_literals

import requests
from tls import request as tls_request

from .models import Visitor
from .affiliations_settings import AFFILIATE_SESSION_KEY


def complete_trigger(request, affiliate_trigger_name):
    """
    Following are actions for when the trigger preconditions has been met.

    - Check whether the affiliate_visitor of the request has a value.
    - If the visitor is found, check that the partner of the visitor is active,
    and that it is subscribed to the trigger with the provided name. If not, do
    not proceed.
    - Do a callback to the partner subscription callback_url, after properly
    substituting the visitor_id on the URL.
    - Call succeed on the visitor, with the user of the request as an argument,
    - Unset the AFFILIATE_SESSION_KEY in the request session, as we now
    consider the affiliate reference business done.

    :param request: request argument as found via the tls module
    :param affiliate_trigger_name:
    :return:
    """
    if hasattr(request, 'affiliate_visitor'):
        visitor = Visitor.objects.filter(
            pk=request.affiliate_visitor.pk
        ).first()
        if visitor:
            partner = visitor.partner
            if partner.active:
                subscription = partner.subscriptions.filter(
                    trigger=affiliate_trigger_name
                ).first()
                if subscription:
                    # Do a callback to the partner subscription callback_url,
                    # after properly substituting the visitor_id on the URL.
                    requests.get(
                        subscription.callback_url.format(visitor_id=visitor.pk)
                    )
                    # Call succeed on the visitor, with the user of the request
                    # as an argument
                    visitor.succeed(request.user)
                    # Unset the AFFILIATE_SESSION_KEY in the request session,
                    # as we now consider the affiliate reference business done
                    del(request.session[AFFILIATE_SESSION_KEY])


def object_created(
        sender,
        instance,
        affiliate_trigger_name,
        created=None,
        **kwargs
):
    """
    Trigger for object creation.

    This trigger has a simple precondition: Check if created for the signal is
    True. If so, call the complete_trigger function, with the request argument
    as found via the tls module, along with the affiliate_trigger_name provided
    to itself.

    :param sender:
    :param instance:
    :param affiliate_trigger_name:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        complete_trigger(tls_request, affiliate_trigger_name)


def object_saved(
        sender,
        instance,
        affiliate_trigger_name,
        created=None,
        **kwargs
):
    """
    Trigger when saving an object.

    This trigger has no preconditions. Just call the complete_trigger function,
    with the request argument as found via the tls module, along with the
    affiliate_trigger_name provided to itself.

    :param sender:
    :param instance:
    :param affiliate_trigger_name:
    :param created:
    :param kwargs:
    :return:
    """
    complete_trigger(tls_request, affiliate_trigger_name)
