# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misago_categories', '0004_category_last_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='require_edits_approval',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='require_replies_approval',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='require_threads_approval',
            field=models.BooleanField(default=False),
        ),
    ]
