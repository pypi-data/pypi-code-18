# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 18:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0060_auto_20160310_0950'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='translation',
            unique_together=set([('subproject', 'language')]),
        ),
    ]
