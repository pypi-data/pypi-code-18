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
"""Test tree item filters.
"""
import unittest

from zope.interface import directlyProvides
from zope.interface.interface import InterfaceClass

from zope.app.tree.filters import OnlyInterfacesFilter, AllButInterfacesFilter

from .test_adapters import SampleContent

IRobot = InterfaceClass('IRobot', (), {})
IHuman = InterfaceClass('IHuman', (), {})
IAlien = InterfaceClass('IAlien', (), {})
ISpaceShipCaptain = InterfaceClass('ISpaceShipCaptain', (), {})
IDeliveryBoy = InterfaceClass('IDeliveryBoy', (IHuman,), {})
IProfessor = InterfaceClass('IProfessor', (IHuman,), {})

class FilterTestCase(unittest.TestCase):

    def setUp(self):
        self.makeObjects()

    def makeObjects(self):
        to_be_made = {
            'bender':      IRobot,
            'fry':         IDeliveryBoy,
            'farnesworth': IProfessor,
            'zapp':        (IHuman, ISpaceShipCaptain),
            'lur':         (IAlien, ISpaceShipCaptain),
            'kif':         IAlien,
        }
        self.items = items = {}
        for name, iface in to_be_made.items():
            items[name] = obj = SampleContent()
            directlyProvides(obj, iface)

    def filterAndCompare(self, filter, expected):
        items = self.items
        result = [name for name, obj in items.items()
                  if filter.matches(obj)]
        for name in expected:
            self.assertIn(name, result)
            result.remove(name)
        self.assertEqual(len(result), 0)

    def test_only_interfaces_filter(self):
        filter = OnlyInterfacesFilter(IHuman)
        self.filterAndCompare(filter,
                              ('fry', 'farnesworth', 'zapp'))

        # even if we add delivery boy to it, the list shouldn't change
        filter = OnlyInterfacesFilter(IHuman, IDeliveryBoy)
        self.filterAndCompare(filter,
                              ('fry', 'farnesworth', 'zapp'))

        # Lur from Omicron Persei 8 is a starship captain too
        # (he also likes to eating hippies and destroying earth)
        filter = OnlyInterfacesFilter(IHuman, ISpaceShipCaptain)
        self.filterAndCompare(filter,
                              ('fry', 'farnesworth', 'zapp', 'lur'))

    def test_all_but_interfaces_filter(self):
        # "death to all humans!"
        filter = AllButInterfacesFilter(IHuman)
        self.filterAndCompare(filter, ('lur', 'kif', 'bender'))

        # and to all spaceship captains...
        filter = AllButInterfacesFilter(IHuman, ISpaceShipCaptain)
        self.filterAndCompare(filter, ('kif', 'bender'))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
