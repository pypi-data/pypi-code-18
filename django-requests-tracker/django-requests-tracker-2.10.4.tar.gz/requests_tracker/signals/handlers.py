"""
requests_tracker.signals.handlers
=================================
"""
import logging
from urlparse import urlsplit, urlunsplit

from requests_tracker import states
from requests_tracker.models import HttpMessage, Record
from requests_tracker.utils import http_message
from requests_tracker.filtering import filters

logger = logging.getLogger(__name__)


def pre_send_handler(sender, uid, prep, identity, **kwargs):
    """handle `requests_tracker.signals.pre_send` signal"""

    setattr(prep, 'identity', identity)

    if filters.rt_filter(prep):
        request_message = HttpMessage.objects.create(
            content=http_message.render_request_message(prep)
        )
        rt_kwargs = {
            'uid': uid,
            'identity': identity or '',
            'method': prep.method,
            'request_message': request_message,
        }

        _ = urlsplit(prep.url)
        rt_kwargs.update({
            'url': urlunsplit((_.scheme, _.netloc, _.path, '', '')),
        })

        record = Record(**rt_kwargs)
        record.save()

        record.transit(states.IN_PROGRESS)


def response_handler(sender, uid, resp, duration, **kwargs):
    """handle `requests_tracker.signals.response` signal"""

    try:
        record = Record.objects.get(uid=uid)
    except Record.DoesNotExist:
        logger.info("uid does not exist: %r" % uid)
    else:
        response_message = HttpMessage.objects.create(
            content=http_message.render_response_message(resp)
        )
        rt_kwargs = {
            'status_code': resp.status_code,
            'response_message': response_message,
            'remark': resp.reason,
            'duration': duration,
        }
        record.transit(states.SUCCESS, **rt_kwargs)


def request_failed_handler(sender, uid, exception, duration, **kwargs):
    """handle `requests_tracker.signals.request_failed` signal"""

    try:
        record = Record.objects.get(uid=uid)
    except Record.DoesNotExist:
        logger.info("uid does not exist: %r" % uid)
    else:
        response_message = HttpMessage.objects.create(
            content=exception.message
        )
        rt_kwargs = {
            'duration': duration,
            'remark': exception.__class__.__name__,
            'response_message': response_message,
        }
        record.transit(states.FAILURE, **rt_kwargs)

    raise exception
