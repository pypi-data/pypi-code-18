# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speeches', '0002_auto_20151112_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speech',
            name='section',
            field=models.ForeignKey(blank=True, to='speeches.Section', help_text=b'The section that this speech is contained in', null=True, verbose_name='Section'),
        ),
    ]
