from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from decimal import Decimal


@python_2_unicode_compatible
class Rating(models.Model):
    votes = models.PositiveIntegerField(_('Amount of vouts'), default=0)
    total = models.PositiveIntegerField(_('Sum of votes'), default=0)
    average = models.DecimalField(
        _('Average rating'),
        max_digits=2, decimal_places=1, default=Decimal(0.0)
    )

    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='ratings',
        verbose_name=_('user'),
        blank=True
    )

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")

    def __str__(self):
        return u"Rating of %s" % self.content_object
