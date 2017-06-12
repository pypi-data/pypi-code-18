import calendar

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import fields as generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from aa_intercom.signals import account_post_save, intercom_event_push_to_intercom_post_save


class IntercomEvent(models.Model):
    """
        Fill types per project.
        Example usage in test_project.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="intercom_events", null=True, blank=True,
                             on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=settings.INTERCOM_EVENT_TYPES)
    text_content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey("content_type", "object_id")
    is_sent = models.BooleanField(default=False)
    # see: https://developers.intercom.com/v2.0/reference#event-model
    metadata = JSONField(help_text=_("Optional metadata about the event"))

    def get_intercom_data(self):
        """Specify the data sent to Intercom API according to event type"""
        data = {
            "event_name": self.get_type_display(),  # event type
            "created_at": calendar.timegm(self.created.utctimetuple()),  # date
            "metadata": self.metadata
        }
        if self.user:
            data["user_id"] = self.user.intercom_id
        return data


post_save.connect(account_post_save, sender=get_user_model())
post_save.connect(intercom_event_push_to_intercom_post_save, sender=IntercomEvent)
