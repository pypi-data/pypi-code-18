#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: uiapp.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Gtk.Application instance

import os
import sys
import subprocess
from datetime import datetime

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Pango
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio

from .service import Service
from .window import GtkAppWindow
from .log import get_logger
from .env import FILE, APP

class UIApp(Gtk.Application):
    """
    """
    def __init__(self, controller):
        Gtk.Application.__init__(self,
                                 application_id="net.t00mlabs.basico",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name("Basico")
        GLib.set_prgname('basico')
        self.log = get_logger(self.__class__.__name__, FILE['LOG'])
        self.controller = controller
        self.get_services()


    def get_services(self):
        self.gui = self.controller.get_service('GUI')
        self.im = self.controller.get_service('IM')
        self.cb = self.controller.get_service('Callbacks')


    def do_activate(self):
        self.window = GtkAppWindow(self)
        self.window.connect("delete-event", self.gui.quit)
        self.window.show()


    def do_startup(self):
        Gtk.Application.do_startup(self)

        # show icons on the buttons
        #~ settings = Gtk.Settings.get_default()
        #~ DEPRECATED: settings.props.gtk_button_images = True

        # actions that control the application: create, connect their
        # signal to a callback method (see below), add the action to the
        # application


    def get_window(self):
        return self


    def get_controller(self):
        return self.controller


    def cb_hide_about(self, aboutdialog, user_data):
        aboutdialog.destroy()


    def cb_toggle_fullscreen(self, tgbutton, user_data=None):
        if tgbutton.get_active():
            self.window.fullscreen()
        else:
            self.window.unfullscreen()


    def cb_show_about(self, *args):
        DIR_ICONS = self.controller.get_var("ICONS")
        CREDITS = self.controller.get_file("CREDITS")
        rootwin = self.gui.get_widget('mainwindow')
        version = APP['version']

        aboutdialog = Gtk.AboutDialog()
        aboutdialog.set_hide_titlebar_when_maximized(True)
        icon_dlg = self.im.get_icon('basico', 96, 96)
        applicense = Gtk.License(Gtk.License.GPL_3_0)
        shortname = self.controller.get_app_info('short')
        longname = self.controller.get_app_info('desc')
        authors = self.controller.get_app_info('authors')
        aboutdialog.set_logo(icon_dlg)
        aboutdialog.set_icon(icon_dlg)
        aboutdialog.set_comments(longname)
        aboutdialog.set_version(version)
        aboutdialog.set_copyright("Copyright \xa9 2016 Tomás Vírseda García")
        aboutdialog.set_license_type(applicense)
        aboutdialog.set_authors(authors)
        aboutdialog.set_website("http://t00mlabs.net")
        aboutdialog.set_website_label("t00mlabs Website")
        aboutdialog.set_title("")
        aboutdialog.connect("response", self.cb_hide_about)
        aboutdialog.set_transient_for(rootwin)
        aboutdialog.set_modal(True)
        aboutdialog.show()
