# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def reasing_recipients(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    TransactionalEmail = apps.get_model('local_sendgrid', 'TransactionalEmail')
    for email in TransactionalEmail.objects.all():
        email.recipients.add(email.recipient)
        email.save()


class Migration(migrations.Migration):

    dependencies = [
        ('local_sendgrid', '0006_auto_20170616_1349'),
    ]

    operations = [
        migrations.RunPython(reasing_recipients),
    ]
