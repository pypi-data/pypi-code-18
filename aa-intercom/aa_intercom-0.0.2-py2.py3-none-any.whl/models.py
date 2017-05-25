from aa_intercom.signals import intercom_event_push_to_intercom_post_save
from django.conf import settings
from django.contrib.contenttypes import fields as generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class IntercomEvent(models.Model):
    """
        Fill types per project.
        Example usage in tests.
    """
    TYPE_EXAMPLE_EVENT = "example_event"
    TYPE_GENERIC = "generic"

    LABEL_EXAMPLE_EVENT = _("example event")
    LABEL_GENERIC = _("generic event")

    EVENT_TYPES = (
        (TYPE_EXAMPLE_EVENT, LABEL_EXAMPLE_EVENT),
        (TYPE_GENERIC, LABEL_GENERIC)
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="intercom_events", null=True, blank=True,
                             on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=EVENT_TYPES)
    text_content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey("content_type", "object_id")
    is_sent = models.BooleanField(default=False)

    class Meta:
        app_label = "aa_intercom"


post_save.connect(intercom_event_push_to_intercom_post_save, sender=IntercomEvent)
