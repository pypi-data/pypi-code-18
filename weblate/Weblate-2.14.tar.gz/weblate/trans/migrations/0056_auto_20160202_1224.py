# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-02 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0055_auto_20160202_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indexupdate',
            name='unit',
        ),
        migrations.AlterField(
            model_name='indexupdate',
            name='unitid',
            field=models.IntegerField(unique=True),
        ),
    ]
