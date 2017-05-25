from django.conf import settings
from django.db import models


class IntercomUserMixin(models.Model):
    """Add fields required by aa_intercom to the user model"""
    intercom_last_api_response = models.TextField(blank=True, null=True)
    intercom_api_response_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def intercom_id(self):
        return "%s_%s" % (settings.INTERCOM_ID_PREFIX, self.pk)
