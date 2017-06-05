import calendar

from django.conf import settings
from django.contrib.contenttypes import fields as generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AbstractIntercomEvent(models.Model):
    """
        Fill types per project.
        Example usage in test_project.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="intercom_events", null=True, blank=True,
                             on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=())
    text_content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey("content_type", "object_id")
    is_sent = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def get_intercom_data(self):
        """Specify the data sent to Intercom API according to event type"""
        data = {
            "event_name": self.get_type_display(),  # event type
            "created_at": calendar.timegm(self.created.utctimetuple()),  # date
            "metadata": {}
        }
        if self.user:
            data["user_id"] = self.user.intercom_id
        return data
