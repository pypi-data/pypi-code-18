# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IntercomEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, choices=[(b'example_event', 'example event'), (b'generic', 'generic event')])),
                ('text_content', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('is_sent', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', on_delete=models.deletion.CASCADE, null=True)),
                ('user', models.ForeignKey(related_name='intercom_events', on_delete=models.deletion.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
