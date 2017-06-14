from __future__ import absolute_import

import datetime
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .conf import settings


class SessionActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session_key = models.CharField(_("session key"), max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    time_logout = models.DateTimeField(null=True)

    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(null=True)

    class Meta:
        verbose_name = _("Session activity")
        verbose_name_plural = _("Session activity")


def create_session_activity(request, user, **kwargs):
    """
    Start session activity tracking for newly logged-in user.
    """
    session = request.session

    if user.is_authenticated() and session.session_key:
        SessionActivity.objects.get_or_create(
            user=user,
            session_key=session.session_key,
            ip_address=request.META.get("REMOTE_ADDR", None),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )


def end_session_activity(request, user, **kwargs):
    """
    Marks end of the session activity.
    Should be called when user logs out or when a session is deactivated.
    """
    session_key = request.session.session_key
    if session_key:
        SessionActivity.objects.filter(session_key=session_key).update(
            time_logout=datetime.datetime.now()
        )


user_logged_in.connect(create_session_activity)
user_logged_out.connect(end_session_activity)
