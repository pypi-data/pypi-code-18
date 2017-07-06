from link.models import Link

from navbuilder import models


def load_fixtures(kls):
    kls.menu_data = {
        "title": "Menu 1",
        "slug": "menu-1"
    }
    kls.menu = models.Menu.objects.create(**kls.menu_data)
 
    kls.link_data = {
        "title": "Link 1",
        "slug": "link-1",
        "url": "/link/1/"
    }
    kls.link = Link.objects.create(**kls.link_data)

    kls.menuitem_data = {
        "title": "Menu Item 1",
        "slug": "menu-item-1",
        "position": 1,
        "menu": kls.menu,
        "link": kls.link
    }
    kls.menuitem = models.MenuItem.objects.create(**kls.menuitem_data)

    kls.sub_menuitem_data = {
        "title": "Sub Menu Item 1",
        "slug": "sub-menu-item-1",
        "position": 1,
        "parent": kls.menuitem,
        "target": "blank",
        "link": kls.link
    }
    kls.sub_menuitem = models.MenuItem.objects.create(
        **kls.sub_menuitem_data
    )


def load_crumb_fixtures(kls):
    kls.menu_data_2 = {
        "title": "Menu 2",
        "slug": "menu-2"
    }
    kls.menu_2 = models.Menu.objects.create(**kls.menu_data_2)

    kls.link_data_2 = {
        "title": "Link 2",
        "slug": "link-2",
        "url": "/link/2/"
    }
    kls.link_2 = Link.objects.create(**kls.link_data_2)

    kls.menuitem_data_2 = {
        "title": "Menu Item 2",
        "slug": "menu-item-2",
        "position": 2,
        "menu": kls.menu_2,
        "link": kls.link
    }
    kls.menuitem_2 = models.MenuItem.objects.create(**kls.menuitem_data_2)

    kls.sub_menuitem_data_2 = {
        "title": "Sub Menu Item 2",
        "slug": "sub-menu-item-2",
        "position": 2,
        "parent": kls.menuitem_2,
        "target": "blank",
        "link": None
    }
    kls.sub_menuitem_2 = models.MenuItem.objects.create(
        **kls.sub_menuitem_data_2
    )
