# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invalidation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text=b'cache key', max_length=255, db_index=True)),
                ('object_id', models.IntegerField()),
                ('sql', models.TextField(null=True)),
                ('count', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('class_name', models.CharField(max_length=255, null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
        ),
        migrations.AlterIndexTogether(
            name='invalidation',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
