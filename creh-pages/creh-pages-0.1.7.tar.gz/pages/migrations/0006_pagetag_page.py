# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20170608_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagetag',
            name='page',
            field=models.ForeignKey(default=1, to='pages.Page'),
            preserve_default=False,
        ),
    ]
