# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unach_photo_server', '0005_auto_20170427_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='photorepository',
            name='is_blob',
            field=models.BooleanField(default=False),
        ),
    ]
