# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.behavior.internalnumber')

REGISTRY_KEY = 'collective.behavior.internalnumber.browser.settings.IInternalNumberConfig'
TYPE_CONFIG = '%s.portal_type_config' % REGISTRY_KEY
