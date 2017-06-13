#############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Menu ZCML directives
"""
from zope.interface import Interface
from zope.configuration.fields import GlobalObject, GlobalInterface
from zope.configuration.fields import Tokens, Path, PythonIdentifier, MessageID
from zope.schema import TextLine, Id, Int, Bool
from zope.security.zcml import Permission

from zope.component.zcml import IBasicViewInformation
from zope.browsermenu.field import MenuField
from ._compat import _u


class IMenuDirective(Interface):
    """Define a browser menu"""

    id = TextLine(
        title=_u("The name of the menu."),
        description=_u("This is, effectively, an id."),
        required=False
        )

    title = MessageID(
        title=_u("Title"),
        description=_u("A descriptive title for documentation purposes"),
        required=False
        )

    description = MessageID(
        title=_u("Description"),
        description=_u("A description title of the menu."),
        required=False
        )

    class_ = GlobalObject(
        title=_u("Menu Class"),
        description=_u("The menu class used to generate the menu."),
        required=False
        )

    interface = GlobalInterface(
        title=_u("The menu's interface."),
        required=False
        )


class IMenuItemsDirective(Interface):
    """
    Define a group of browser menu items

    This directive is useful when many menu items are defined for the
    same interface and menu.
    """

    menu = MenuField(
        title=_u("Menu name"),
        description=_u("The (name of the) menu the items are defined for"),
        required=True,
        )

    for_ = GlobalObject(
        title=_u("Interface"),
        description=_u("The interface the menu items are defined for"),
        required=True
        )

    layer = GlobalInterface(
        title=_u("Layer"),
        description=_u("The Layer for which the item is declared."),
        required=False
        )

    permission = Permission(
        title=_u("The permission needed access the item"),
        description=_u("""
        This can usually be inferred by the system, however, doing so
        may be expensive. When displaying a menu, the system tries to
        traverse to the URLs given in each action to determine whether
        the url is accessible to the current user. This can be
        avoided if the permission is given explicitly."""),
        required=False
        )


class IMenuItem(Interface):
    """Common menu item configuration
    """

    title = MessageID(
        title=_u("Title"),
        description=_u("The text to be displayed for the menu item"),
        required=True
        )

    description = MessageID(
        title=_u("A longer explanation of the menu item"),
        description=_u("""
        A UI may display this with the item or display it when the
        user requests more assistance."""),
        required=False
        )

    icon = TextLine(
        title=_u("Icon Path"),
        description=_u("Path to the icon resource representing this menu item."),
        required=False
        )

    permission = Permission(
        title=_u("The permission needed access the item"),
        description=_u("""
        This can usually be inferred by the system, however, doing so
        may be expensive. When displaying a menu, the system tries to
        traverse to the URLs given in each action to determine whether
        the url is accessible to the current user. This can be
        avoided if the permission is given explicitly."""),
        required=False
        )

    filter = TextLine(
        title=_u("A condition for displaying the menu item"),
        description=_u("""
        The condition is given as a TALES expression. The expression
        has access to the variables:

        context -- The object the menu is being displayed for

        request -- The browser request

        nothing -- None

        The menu item will not be displayed if there is a filter and
        the filter evaluates to a false value."""),
        required=False
        )

    order = Int(
        title=_u("Order"),
        description=_u("A relative position of the menu item in the menu."),
        required=False,
        default=0
        )

    item_class = GlobalObject(
        title=_u("Menu item class"),
        description=_u("""
        A class to be used as a factory for creating menu item"""),
        required=False
        )

class IMenuItemSubdirective(IMenuItem):
    """Define a menu item within a group of menu items"""

    action = TextLine(
        title=_u("The relative url to use if the item is selected"),
        description=_u("""
        The url is relative to the object the menu is being displayed
        for."""),
        required=True
        )

class IMenuItemDirective(IMenuItemsDirective, IMenuItemSubdirective):
    """Define one menu item"""

class ISubMenuItemSubdirective(IMenuItem):
    """Define a menu item that represents a a sub menu.

    For a sub-menu menu item, the action is optional, this the item itself
    might not represent a destination, but just an entry point to the sub menu.
    """

    action = TextLine(
        title=_u("The relative url to use if the item is selected"),
        description=_u("""
        The url is relative to the object the menu is being displayed
        for."""),
        required=False
        )

    submenu = TextLine(
        title=_u("Sub-Menu Id"),
        description=_u("The menu that will be used to provide the sub-entries."),
        required=True,
        )

class ISubMenuItemDirective(IMenuItemsDirective, ISubMenuItemSubdirective):
    """Define one menu item"""

class IAddMenuItemDirective(IMenuItem):
    """Define an add-menu item"""

    for_ = GlobalInterface(
        title=_u("Interface"),
        description=_u("The interface the menu items are defined for"),
        required=False
        )

    class_ = GlobalObject(
        title=_u("Class"),
        description=_u("""
        A class to be used as a factory for creating new objects"""),
        required=False
        )

    factory = Id(
        title=_u("Factory"),
        description=_u("A factory id for creating new objects"),
        required = False,
        )

    view = TextLine(
        title=_u("Custom view name"),
        description=_u("The name of a custom add view"),
        required = False,
        )

    menu = MenuField(
        title=_u("Menu name"),
        description=_u("The (name of the) menu the items are defined for"),
        required=False,
        )

    layer = GlobalInterface(
        title=_u("The layer the custom view is declared for"),
        description=_u("The default layer for which the custom view is "
                       "applicable. By default it is applied to all layers."),
        required=False
        )
