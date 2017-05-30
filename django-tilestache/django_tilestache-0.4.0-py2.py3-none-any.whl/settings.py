"""Django Tilestache main settings"""
# coding: utf-8
import os
from django.conf import settings
from appconf import AppConf


class DjangoTilestacheSettings(AppConf):

    FILE_CONF = os.path.join(settings.BASE_DIR, 'tilestache.cfg')
    CONF_CACHE = 1  # minutes
    AUTOGENERATE_FILE = True

    class Meta:
        # prefix for these variables
        # this will become TILESTACHE_FILE_CONF in your settings.py
        prefix = 'tilestache'
        proxy = True
