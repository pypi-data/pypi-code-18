# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import squad.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_build_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='version',
            field=squad.core.fields.VersionField(),
        ),
    ]
