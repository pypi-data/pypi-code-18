# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 07:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import weblate.screenshots.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trans', '0074_auto_20170209_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Screenshot name')),
                ('image', weblate.screenshots.fields.ScreenshotField(blank=True, help_text='Upload JPEG or PNG images up to 2000x2000 pixels.', upload_to='screenshots/', verbose_name='Image')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trans.SubProject')),
                ('sources', models.ManyToManyField(blank=True, related_name='screenshots', to='trans.Source')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
