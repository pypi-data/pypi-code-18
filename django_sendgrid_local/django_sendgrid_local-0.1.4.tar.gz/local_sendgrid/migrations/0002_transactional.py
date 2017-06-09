# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('local_sendgrid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactional',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('html_content', models.TextField()),
                ('plain_content', models.TextField()),
                ('template_id', models.IntegerField()),
                ('category', models.CharField(max_length=255)),
                ('recipient', models.ForeignKey(to='local_sendgrid.Contact')),
            ],
        ),
    ]
