# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visit_date', models.DateField(verbose_name='Data wizyty')),
                ('guest', models.CharField(max_length=150, verbose_name='Imi\u0119 i nazwisko go\u015bcia')),
                ('company', models.CharField(max_length=150, verbose_name='Firma kt\xf3r\u0105 reprezentuje', blank=True)),
                ('visit_host', models.CharField(max_length=150, verbose_name='Do kogo')),
                ('plan_hour', models.TimeField(default=datetime.time(0, 0), verbose_name='Planowana godzina wizyty')),
                ('arrive_hour', models.TimeField(null=True, verbose_name='Godzina przybycia', blank=True)),
                ('exit_hour', models.TimeField(null=True, verbose_name='Godzina wyj\u015bcia', blank=True)),
                ('coffe', models.NullBooleanField(verbose_name='Kawa')),
                ('lunch', models.NullBooleanField(verbose_name='Lunch')),
                ('comment', models.TextField(max_length=250, verbose_name='Komentarz', blank=True)),
                ('key_in_user', models.ForeignKey(verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
