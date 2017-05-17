# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-10 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0059_auto_20160303_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='action',
            field=models.IntegerField(choices=[(0, 'Resource update'), (1, 'Translation completed'), (2, 'Translation changed'), (5, 'New translation'), (3, 'Comment added'), (4, 'Suggestion added'), (6, 'Automatic translation'), (7, 'Suggestion accepted'), (8, 'Translation reverted'), (9, 'Translation uploaded'), (10, 'Glossary added'), (11, 'Glossary updated'), (12, 'Glossary uploaded'), (13, 'New source string'), (14, 'Component locked'), (15, 'Component unlocked'), (16, 'Detected duplicate string'), (17, 'Commited changes'), (18, 'Pushed changes'), (19, 'Reset repository'), (20, 'Merged repository'), (21, 'Rebased repository'), (22, 'Failed merge on repository'), (23, 'Failed rebase on repository'), (24, 'Parse error')], default=2),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='new_lang',
            field=models.CharField(choices=[('contact', 'Use contact form'), ('url', 'Point to translation instructions URL'), ('add', 'Automatically add language file'), ('none', 'No adding of language')], default='add', help_text='How to handle requests for creating new translations. Please note that availability of choices depends on the file format.', max_length=10, verbose_name='New translation'),
        ),
    ]
