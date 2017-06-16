# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('local_sendgrid', '0003_auto_20170608_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionalemail',
            name='template_id',
            field=models.CharField(max_length=255),
        ),
    ]
