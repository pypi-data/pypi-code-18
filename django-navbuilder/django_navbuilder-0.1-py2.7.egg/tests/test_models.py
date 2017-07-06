from django.test import TestCase

from navbuilder.models import Menu, MenuItem
from navbuilder.tests.test_base import load_fixtures


class ModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(ModelTestCase, cls).setUpTestData()
        load_fixtures(cls)

    def test_link(self):
        for key, value in self.link_data.items():
            self.assertEqual(getattr(self.link, key), value)

    def test_menu(self):
        for key, value in self.menu_data.items():
            self.assertEqual(getattr(self.menu, key), value)
        self.assertEqual(unicode(self.menu), self.menu.title)

    def test_menuitem(self):
        for key, value in self.menuitem_data.items():
            self.assertEqual(getattr(self.menuitem, key), value)
        for key, value in self.sub_menuitem_data.items():
            self.assertEqual(getattr(self.sub_menuitem, key), value)
        self.assertEqual(self.sub_menuitem.parent, self.menuitem)
        self.assertEqual(unicode(self.menuitem), self.menuitem.title)
        self.assertEqual(self.sub_menuitem.root_menu, self.menuitem.menu)

        # Change the menuitem's menu and confirm root_menu is updated
        other = Menu.objects.create(title="Other", slug="other")
        self.menuitem.menu = other
        self.menuitem.save()
        # Re-fetch sub_menuitem because it is effectively cached
        self.sub_menuitem = MenuItem.objects.get(id=self.sub_menuitem.id)
        self.assertEqual(self.menuitem.root_menu, other)
        self.assertEqual(self.sub_menuitem.root_menu, other)
