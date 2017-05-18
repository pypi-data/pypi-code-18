# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=500)),
                ('sender', models.IntegerField(null=True)),
                ('html_content', models.TextField()),
                ('plain_content', models.TextField()),
                ('sendgrid_id', models.CharField(max_length=255, unique=True, null=True, editable=False, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('timestamp', models.CharField(max_length=255, null=True, blank=True)),
                ('sg_message_id', models.CharField(max_length=255, null=True, blank=True)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('category', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255)),
                ('sendgrid_id', models.CharField(unique=True, max_length=255, editable=False, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('sendgrid_id', models.CharField(max_length=255, unique=True, null=True, editable=False, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delivered',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('timestamp', models.CharField(max_length=255, null=True, blank=True)),
                ('sg_message_id', models.CharField(max_length=255, null=True, blank=True)),
                ('smtp_id', models.CharField(max_length=255, null=True, blank=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='local_sendgrid.Contact', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Open',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('timestamp', models.CharField(max_length=255, null=True, blank=True)),
                ('sg_message_id', models.CharField(max_length=255, null=True, blank=True)),
                ('ip', models.CharField(max_length=255, null=True, blank=True)),
                ('useragent', models.CharField(max_length=255, null=True, blank=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='local_sendgrid.Contact', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_lists',
            field=models.ManyToManyField(to='local_sendgrid.ContactList'),
        ),
        migrations.AddField(
            model_name='click',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='local_sendgrid.Contact', null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='contact_list',
            field=models.ForeignKey(to='local_sendgrid.ContactList', null=True),
        ),
    ]
