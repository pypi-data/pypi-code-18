"""Django models to handle affiliations."""

from __future__ import unicode_literals

from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone

from .exceptions import InvalidCallBackURL


class Partner(models.Model):
    """
    A partner is someone we make an affilate deal with.

    The partner will then generate traffic to the site.
    The initial referral will include the partner uid in the query string,
    to identify the traffic as originating from the particular partner.
    """

    uid = models.CharField(max_length=8, unique=True, editable=False)
    name = models.CharField(max_length=250)
    active = models.BooleanField(default=False)

    def __str__(self):
        """String representation for each instance of the model."""
        return self.name

    def save(self, *args, **kwargs):
        """Overriding the save method to set the uid if required."""
        if not self.uid:
            self.uid = get_random_string(8)

        super(Partner, self).save(*args, **kwargs)


class Subscription(models.Model):
    """A subscription tells which triggers a partner subscribes to."""

    CALLBACK_URL_PLACEHOLDER = '{visitor_id}'
    # the 'name' of one of the triggers defined in the settings.
    trigger = models.CharField(max_length=100)
    partner = models.ForeignKey(Partner, related_name='subscriptions')
    # the partner callback URL. Should have the placeholder
    # {visitor_id} in it somewhere, e.g. as the value for a query
    # string parameter.
    callback_url = models.URLField()

    def __str__(self):
        """String representation for each instance of the model."""
        return self.trigger

    def validate_callback_url(self):
        """
        Validate the callback_url.

        Validate the callback_url which should have the placeholder
        {visitor_id} in it somewhere, e.g. as the value for a query.
        """
        if self.CALLBACK_URL_PLACEHOLDER not in self.callback_url:
            raise InvalidCallBackURL

    def save(self, *args, **kwargs):
        """Overriding the save method to validate the callback_url."""
        if self.callback_url:
            self.validate_callback_url()

        super(Subscription, self).save(*args, **kwargs)


class Visitor(models.Model):
    """
    A visitor is soneone who gets referred to our site by a partner.

    The new middleware will detect that a request
    was caused by an affiliate partner and then register a new visitor.
    """

    partner = models.ForeignKey(Partner, related_name='visitors')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='visitors')
    referred_on = models.DateTimeField(auto_now_add=True)
    # the URL at which the visitor entered our site
    entry_point = models.URLField()
    # tells the date the conditions of a 'success' were met, if at all
    successful_on = models.DateTimeField(null=True)

    def __str__(self):
        """String representation for each instance of the model."""
        return self.entry_point

    def succeed(self, user=None):
        """
        On success state.

        Will set the successful_on to now() and - if user is specified -
        set the user value for the visitor. But this must only happen if the
        value of successful_on is None. We don't want to change the success
        state on already successful affiliate visitors.
        """
        if not self.successful_on:
            self.successful_on = timezone.now()
            if user:
                self.user = user
            self.save()
