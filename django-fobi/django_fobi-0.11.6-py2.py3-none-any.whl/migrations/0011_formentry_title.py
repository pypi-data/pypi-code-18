# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-08 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fobi', '0010_formwizardhandler'),
    ]

    operations = [
        migrations.AddField(
            model_name='formentry',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title'),
        ),
    ]
