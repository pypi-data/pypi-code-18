# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('local_sendgrid', '0002_transactional'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionalEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('html_content', models.TextField()),
                ('plain_content', models.TextField()),
                ('template_id', models.IntegerField()),
                ('category', models.CharField(max_length=255)),
                ('recipient', models.ForeignKey(to='local_sendgrid.Contact')),
            ],
        ),
        migrations.RemoveField(
            model_name='transactional',
            name='recipient',
        ),
        migrations.DeleteModel(
            name='Transactional',
        ),
    ]
