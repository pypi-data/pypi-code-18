from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.utils import timezone
from ipware.ip import get_real_ip
import logging


logger = logging.getLogger(__name__)


# If this gets more complex - maybe consider a class so it can be extended

def get_client_ip(request):
    """ Try to get request's ip address even when behind cdn """
    return get_real_ip(request)


def should_log_user(user):
    if user is not None and user.is_staff:
        return True
    return False


def build_auth_log_string(message: str, user, request):
    """ Build a string with user and auth info for logging """
    return "{} {} {} {}".format(
        message,
        user,
        get_client_ip(request),
        timezone.now(),
    )


def handle_user_logged_in(sender, user=None, request=None, **kwargs):
    if should_log_user(user):
        log_string = build_auth_log_string(
            "User login successful",
            user,
            request,
        )
        logger.info(log_string)


def handle_user_login_failed(sender, user=None, request=None, **kwargs):
    if should_log_user(user):
        log_string = build_auth_log_string(
            "User login failed",
            user,
            request,
        )
        logger.info(log_string)

user_logged_in.connect(handle_user_logged_in)
user_login_failed.connect(handle_user_login_failed)
