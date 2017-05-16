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
"""Object adapters

This module contains adapters necessary to use common objects with
statictree. The most prominent ones are those for ILocation and
IContainer. We also provide adapters for any object, so we don't end
up with ComponentLookupErrors whenever encounter unknown objects.


"""

from zope.interface import Interface, implementer
from zope.component import adapter
from zope.security import canAccess
from zope.security.interfaces import Unauthorized
from zope.location.interfaces import ILocation
from zope.traversing.api import getParents

from zope.container.interfaces import IReadContainer

from zope.app.tree.interfaces import IUniqueId, IChildObjects

import zope.component.interfaces

@implementer(IUniqueId)
@adapter(Interface)
class StubUniqueId(object):

    def __init__(self, context):
        self.context = context

    def getId(self):
        # this does not work for persistent objects
        return str(id(self.context))


@implementer(IChildObjects)
@adapter(Interface)
class StubChildObjects(object):

    def __init__(self, context):
        pass

    def hasChildren(self):
        return False

    def getChildObjects(self):
        return []

@implementer(IUniqueId)
@adapter(ILocation)
class LocationUniqueId(object):

    def __init__(self, context):
        self.context = context

    def getId(self):
        context = self.context
        if not context.__name__:
            # always try to be unique
            return str(id(context))
        parents = [context.__name__]
        parents += [parent.__name__ for parent in getParents(context)
                    if parent.__name__]
        return '\\'.join(parents)

@implementer(IChildObjects)
@adapter(IReadContainer)
class ContainerChildObjects(object):

    def __init__(self, context):
        self.context = context

    def hasChildren(self):
        # make sure we check for access
        try:
            return bool(len(self.context))
        except Unauthorized: # pragma: no cover
            return False

    def getChildObjects(self):
        return list(self.context.values()) if self.hasChildren() else []


@adapter(zope.component.interfaces.ISite)
class ContainerSiteChildObjects(ContainerChildObjects):
    """Adapter for read containers which are sites as well. The site
    manager will be treated as just another child object.
    """

    def hasChildren(self):
        if super(ContainerSiteChildObjects, self).hasChildren():
            return True
        return self._canAccessSiteManager()

    def getChildObjects(self):
        if not self.hasChildren():
            return []

        values = super(ContainerSiteChildObjects, self).getChildObjects()
        if self._canAccessSiteManager():
            return [self.context.getSiteManager()] + list(values)
        return values

    def _canAccessSiteManager(self):
        try:
            # the ++etc++ namespace is public this means we get the sitemanager
            # without permissions. But this does not mean we can access it
            # Right now we check the __getitem__ method on the sitemamanger
            # but this means we don't show the ++etc++site link if we have
            # registred views on the sitemanager which have other permission
            # then the __getitem__ method form the interface IReadContainer
            # in the LocalSiteManager.
            # If this will be a problem in the future, we can add a
            # attribute to the SiteManager which we can give individual
            # permissions and check it via canAccess.
            sitemanager = self.context.getSiteManager()
            authorized = canAccess(sitemanager, '__getitem__')
            return bool(authorized)
        except zope.component.interfaces.ComponentLookupError:
            return False
        except TypeError: # pragma: no cover
            # we can't check unproxied objects, but unproxied objects
            # are public.
            return True
