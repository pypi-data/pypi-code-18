# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('urls', '0003_auto_20170509_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlredirect',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 1, 19, 9, 434101, tzinfo=utc), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='date_end_validity',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 1, 19, 9, 433976, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='date_initial_validity',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 1, 19, 9, 433918, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 1, 19, 9, 434136, tzinfo=utc), editable=False),
            preserve_default=True,
        ),
    ]
