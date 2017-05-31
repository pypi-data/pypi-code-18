# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from plone.indexer import indexer
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.utils import base_hasattr, safe_unicode
from Products.PluginIndexes.common.UnIndex import _marker as common_marker

from collective import dexteritytextindexer

from .behavior import IInternalNumberBehavior


@indexer(IContentish)
def internal_number_index(obj):
    """ Index method escaping acquisition and ready for ZCatalog 3 """
    if base_hasattr(obj, 'internal_number') and obj.internal_number:
        return obj.internal_number
    return common_marker


class InternalNumberSearchableExtender(object):
    """
        Extends SearchableText of IInternalNumberBehavior objects.
    """
    adapts(IInternalNumberBehavior)
    implements(dexteritytextindexer.IDynamicTextIndexExtender)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return safe_unicode(self.context.internal_number)
