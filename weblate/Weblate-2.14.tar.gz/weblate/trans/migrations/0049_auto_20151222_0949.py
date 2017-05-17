# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-22 09:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lang', '0002_auto_20150630_1208'),
        ('trans', '0048_auto_20151120_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='whiteboardmessage',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lang.Language'),
        ),
        migrations.AddField(
            model_name='whiteboardmessage',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trans.Project'),
        ),
        migrations.AddField(
            model_name='whiteboardmessage',
            name='subproject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trans.SubProject'),
        ),
        migrations.AlterField(
            model_name='whiteboardmessage',
            name='message',
            field=models.TextField(verbose_name='Message'),
        ),
    ]
