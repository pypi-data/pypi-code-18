# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
