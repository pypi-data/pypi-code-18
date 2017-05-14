# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import json

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from . import middlewares


class History(models.Model):
    """
    object change history
    """
    target_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey(
        'target_type', 'target_object_id')
    who = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT)
    uri = models.CharField(max_length=512, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()

    @classmethod
    def serialize_field(self, value):
        return repr(value)

    @classmethod
    def on_change(klass, includes, excludes, sender, instance, **kwargs):
        if not instance.pk or kwargs.get('created'):
            return
        old = instance.__class__.objects.get(pk=instance.pk)
        d = {}
        for f in instance.__class__._meta.get_fields():
            n = getattr(instance, f.name)
            o = getattr(old, f.name)
            if n != o:
                d[f.name] = klass.serialize_field(o), klass.serialize_field(n)
        who, uri = None, None
        th_local = middlewares.GlobalRequestMiddleware.thread_local
        if hasattr(th_local, 'request'):
            who = getattr(th_local.request, 'user', None)
            uri = getattr(th_local.request, 'path', None)
        klass.objects.create(target=instance, who=who, uri=uri, changes=json.dumps(d))


class EmailCategory(models.Model):
    """
    Model to store email category
    """
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmailLog(models.Model):
    """
    Model to store all the outgoing emails.
    """

    when = models.DateTimeField(null=False, auto_now_add=True)
    to = models.EmailField(null=False, blank=False)
    from_email = models.EmailField(null=False, blank=False)
    subject = models.CharField(null=False, max_length=128)
    body = models.TextField(null=False, max_length=1024)
    ok = models.BooleanField(null=False, default=True)
    stack_trace = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=256, blank=True, null=True)
    message_id = models.CharField(max_length=1024, blank=True, null=True)
    request_id = models.CharField(max_length=1024, blank=True, null=True)
    category = models.ForeignKey(EmailCategory, blank=True, null=True)

    bounced = models.BooleanField(null=False, default=False)
    complained = models.BooleanField(null=False, default=False)
    delivered = models.BooleanField(null=False, default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class _EmailLoggerSetAttr(object):
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __call__(self, sender, instance, **kwargs):
        if not kwargs['created']:
            return
        for email in EmailLog.objects.filter(message_id=instance.mail_id):
            setattr(email, self.attr_name, True)
            email.save()


try:
    import django_bouncy  # NOQA
    __cbs = []
    for attr, model_name in [('delivered', 'Delivery'), ('bounced', 'Bounce'), ('complained', 'Complaint')]:
        cb = _EmailLoggerSetAttr(attr)
        models.signals.post_save.connect(
            cb, 'django_bouncy.{}'.format(model_name),
            dispatch_uid='django_busybody.rules._set_{}'.format(attr))
        __cbs.append(cb)
except ImportError:  # pragma: no cover
    pass
