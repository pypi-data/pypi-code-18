# coding: utf-8
import os
from django.conf import settings


def get_tilestache_conf():

    if hasattr(settings, 'TILESTACHE_CONF'):
        return settings.TILESTACHE_CONF

    return os.path.join(settings.BASE_DIR, 'settings', 'tilestache.cfg')
