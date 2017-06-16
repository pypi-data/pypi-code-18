# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('local_sendgrid', '0005_auto_20170609_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionalemail',
            name='recipients',
            field=models.ManyToManyField(to='local_sendgrid.Contact'),
        ),
        migrations.AlterField(
            model_name='transactionalemail',
            name='recipient',
            field=models.ForeignKey(related_name='__recipients', to='local_sendgrid.Contact'),
        ),
    ]
