##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Base Test Case for Tree Tests

"""
import unittest
from zope.interface import implementer, Interface, Attribute
from zope.location import Location

from zope.component.testing import PlacelessSetup
from zope import component as ztapi

from zope.app.tree.interfaces import IUniqueId, IChildObjects, ITreeStateEncoder
from zope.app.tree.node import Node
from zope.app.tree.utils import TreeStateEncoder

class IItem(Interface):
    """Simple object that can have an id and a set of children
    """
    id = Attribute("id")
    children = Attribute("children")


@implementer(IItem)
class Item(Location):

    def __init__(self, id, children=()):
        self.id = id
        self.children = children
        for child in children:
            child.__parent__ = self


@implementer(IUniqueId)
class ItemUniqueId(object):
    """Simplistic adapter from IItem to IUniqueId
    """

    def __init__(self, context):
        self.id = context.id

    def getId(self):
        return self.id


@implementer(IChildObjects)
class ItemChildObjects(object):
    """Simplistic adapter from IItem to IChildObjects
    """

    def __init__(self, context):
        self.children = context.children

    def getChildObjects(self):
        return self.children

    def hasChildren(self):
        return len(self.children) > 0

# function used to convert a set of nested tuples to items and
# children items.
def make_item_from_tuple(item_tuple, dict):
    children = []
    if len(item_tuple) > 1:
        for child in item_tuple[1]:
            children.append(make_item_from_tuple(child, dict))
    item = Item(item_tuple[0], children)
    dict[item_tuple[0]] = item
    return item

tree = ('a', [
           ('b', [
               ('d',), ('e',)
               ]),
           ('c', [
               ('f', [
                   ('h',), ('i',)
                   ]),
               ('g')]
           ) ]
       )

def provideAdapter(required, provided, factory, name='', with_=()):
    required = (required,) + with_

    ztapi.provideAdapter(factory, required, provided, name=name)

def provideUtility(provided, component):
    ztapi.provideUtility(component, provided)

from zope.publisher.interfaces.browser import IDefaultBrowserLayer

def browserView(for_, name, factory, layer=IDefaultBrowserLayer,
                providing=Interface):
    """Define a global browser view
    """
    provideAdapter(for_, providing, factory, name, (layer,))

class BaseTestCase(PlacelessSetup, unittest.TestCase):
    """Base class for most static tree tests
    """

    expanded_nodes = ['a', 'c']

    def setUp(self):
        super(BaseTestCase, self).setUp()
        # provide necessary components
        ztapi.provideAdapter(ItemUniqueId, (IItem,), IUniqueId)
        ztapi.provideAdapter(ItemChildObjects, (IItem,), IChildObjects)
        ztapi.provideUtility(TreeStateEncoder(), ITreeStateEncoder)
        self.items = {}
        self.root_obj = None
        self.root_node = None

    def makeItems(self):
        # this mapping will provide shortcuts to each object
        self.items = {}
        self.root_obj = make_item_from_tuple(tree, self.items)
        self.root_node = Node(self.root_obj, self.expanded_nodes)
