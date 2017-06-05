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
        return "%s_%s" % (getattr(settings, "INTERCOM_ID_PREFIX", ""), self.pk)

    def get_intercom_data(self):
        """Specify the user data sent to Intercom API"""
        return {
            "user_id": self.intercom_id,
            "email": self.email,
            "name": self.get_full_name(),
            "last_request_at": self.last_login.strftime("%s") if self.last_login else "",
            "created_at": self.date_joined.strftime("%s"),
            "custom_attributes": {
                "is_admin": self.is_superuser
            }
        }
