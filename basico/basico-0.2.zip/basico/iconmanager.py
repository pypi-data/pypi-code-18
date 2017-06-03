#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: menus.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Icon manager service

import os

import pkg_resources

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Pango
from gi.repository.GdkPixbuf import Pixbuf

from .service import Service


def resource_filename(file_name):
    paths = map(
        lambda path: os.path.join(path, file_name),
        (
            '/opt/extras.ubuntu.com/',
            '/usr/local/',
            '/usr/',
        ),
    )
    for path in paths:
        if os.path.isfile(path):
            return path
    return pkg_resources.resource_filename(
        pkg_resources.Requirement.parse("basico"), file_name)


class IconManager(Service):
    def initialize(self):
        APP_DIR_ICONS = self.app.get_var('ICONS')
        self.icondict = {}
        self.theme = Gtk.IconTheme.get_default()
        self.theme.prepend_search_path (APP_DIR_ICONS)

    def get_themed_icon(self, icon_name):
        APP_DIR_ICONS = self.app.get_var('ICONS')
        ICON = APP_DIR_ICONS + icon_name + '.png'
        icon = Gio.ThemedIcon.new(ICON)

        return icon



    def get_icon(self, name, width=24, height=24):
        key = "%s-%d-%d" % (name, width, height)

        # Get icon from cache if exists or add a new one
        try:
            icon = self.icondict[key]
            #~ print ("ICON TRY: %s: %s" % (type(icon), icon))
        except:
            #~ OLD WAY: icon = Pixbuf.new_from_file_at_scale(icon_name, width, height, True)
            iconinfo = self.theme.lookup_icon(name, width, Gtk.IconLookupFlags.GENERIC_FALLBACK)
            icon = iconinfo.load_icon()
            #~ print ("ICON EXCEPT: %s: %s" % (type(icon), icon))
            self.icondict[key] = icon
            #~ icon = None
        return icon


    def get_pixbuf_icon(self, name, width=36, height=36):
        key = "%s-%d-%d" % (name, width, height)

        # Get icon from cache if exists or add a new one
        try:
            icon = self.icondict[key]
        except:
            icon = None
            #~ OLD WAY: icon = Pixbuf.new_from_file_at_scale(icon_name, width, height, True)
            #~ fout = open('icons.txt', 'w')
            #~ for icon in self.theme.list_icons():
                #~ fout.write('%s\n' % icon)
            #~ fout.close()
            if name in self.theme.list_icons():
                return self.theme.load_icon(name, width, Gtk.IconLookupFlags.GENERIC_FALLBACK)
            #~ if self.theme.has_icon(name):

            #~ iconinfo = self.theme.lookup_icon(name, width, Gtk.IconLookupFlags.GENERIC_FALLBACK)
            #~ icon = iconinfo.load_icon()
            #~ self.icondict[key] = icon
        return icon


    def get_image_icon(self, name, width=36, height=36):
        pixbuf = self.get_pixbuf_icon(name, width, height)
        return Gtk.Image.new_from_pixbuf(pixbuf)
