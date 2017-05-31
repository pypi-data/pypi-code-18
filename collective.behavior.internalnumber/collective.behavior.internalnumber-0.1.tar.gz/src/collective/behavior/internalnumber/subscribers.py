# -*- coding: utf-8 -*-
"""Subscribers."""

from plone import api
from Products.CMFPlone.utils import base_hasattr

from .browser.settings import get_settings
from . import TYPE_CONFIG


def object_added(obj, event):
    """ Increment the value in registry """
    # internal_number is unknown or empty => no need to increment
    if not base_hasattr(obj, 'internal_number') or not obj.internal_number:
        return
    settings = get_settings()
    pt = obj.portal_type
    if pt in settings:
        settings[pt]['nb'] += 1
    elif 'glo_bal' in settings:
        settings['glo_bal']['nb'] += 1
    else:
        return
    config = []
    for pt in sorted(settings.keys()):
        config.append({'portal_type': pt, 'uniqueness': settings[pt]['u'], 'default_number': settings[pt]['nb'],
                       'default_expression': settings[pt]['expr']})
    api.portal.set_registry_record(TYPE_CONFIG, config)
