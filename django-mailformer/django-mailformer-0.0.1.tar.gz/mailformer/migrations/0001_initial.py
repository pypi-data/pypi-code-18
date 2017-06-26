# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mailformer.models_tools


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False,verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=998)),
                ('message', models.TextField()),
                ('process_after', models.DateTimeField(auto_now_add=True)),
                ('processor', models.CharField(editable=False, max_length=32, null=True)),
                ('returned', models.TextField(editable=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'NEW'), (2, 'PROCESSING'), (3, 'RETRY'), (4, 'ERROR'), (5, 'SENT'), (6, 'INVALID')])),
            ],
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=64, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('salt', models.BinaryField(default=mailformer.models_tools.random_salt)),
            ],
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(to='mailformer.Recipient'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(to='mailformer.Sender'),
        ),
    ]
