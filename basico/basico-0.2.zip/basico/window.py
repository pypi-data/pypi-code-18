#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: window.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Gtk.ApplicationWindow implementation

import os
import stat
import threading
import time
import platform

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import Pango
from gi.repository import WebKit
from gi.repository.GdkPixbuf import Pixbuf

from .log import get_logger
from .sapnoteview import SAPNoteView


MONOSPACE_FONT = 'Lucida Console' if platform.system() == 'Windows' else 'monospace'

class GtkAppWindow(Gtk.ApplicationWindow):
    def __init__(self, uiapp):
        self.setup_controller(uiapp)
        self.get_services()
        self.gui.add_widget('uiapp', uiapp)
        self.gui.set_key('cmbvalue', 'search')
        self.settings = {}
        self.settings['fullscreen'] = False
        self.current_notes = {}

        self.setup_window()
        self.setup_widgets()
        self.setup_app()


    def setup_controller(self, uiapp):
        self.uiapp = uiapp
        self.controller = uiapp.get_controller()


    def setup_app(self):
        sapnoteview = self.gui.get_widget('sapnoteview')
        searchentry = self.gui.get_widget("stySearchInfo")
        viewlabel = self.gui.get_widget('lblViewCurrent')
        try:
            name = sapnoteview.get_view()
        except:
            name = 'components'
        sapnoteview.set_view(name)
        label = "<span size='20000'><b>%-10s</b></span>" % name.capitalize()
        viewlabel.set_markup(label)
        self.cb.refresh_view()
        searchentry.set_text('')
        self.cb.search_notes()
        sapnoteview.check_states()


    def setup_window(self):
        app_title = self.controller.get_app_info('name')
        Gtk.Window.__init__(self, title=app_title, application=self.uiapp)
        self.gui.add_widget('mainwindow', self)
        icon = self.im.get_icon('basico')
        self.set_icon(icon)
        # FIXME
        # From docs: Don’t use this function. It sets the X xlib.Window
        # System “class” and “name” hints for a window.
        # But I have to do it or it doesn't shows the right title. ???
        self.set_wmclass (app_title, app_title)
        self.set_role(app_title)
        self.set_default_size(1024, 728)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        #~ self.connect('destroy', Gtk.main_quit)
        self.show_all()


    def setup_menu_views(self):
        # View label
        self.gui.add_widget('lblViewCurrent')

        ## Views Menu
        views_menu = self.gui.add_widget('mnuviews', Gio.Menu())

        # Last added view
        #~ TODO
        #~ views_menu.append_item(self.uif.create_item('View last added', 'app.view-lastadded', ''))
        #~ self.app.add_action(self.uif.create_action("view-lastadded", self.cb_show_dlnotes_window))

        # Most used view
        #~ TODO
        #~ views_menu.append_item(self.uif.create_item('View most used', 'app.view-mostused', ''))
        #~ self.app.add_action(self.uif.create_action("view-mostused", self.cb_show_dlnotes_window))

        # Tasks view
        views_menu.append_item(self.uif.create_item('View by tasks', 'app.view-tasks', 'emblem-system'))
        self.app.add_action(self.uif.create_action("view-tasks", self.cb.refresh_view, 'tasks'))

        # Projects view
        #~ views_menu.append_item(self.uif.create_item('View by projects', 'app.view-projects', ''))
        #~ self.app.add_action(self.uif.create_action("view-projects", self.cb.refresh_view, 'projects'))

        # Components view
        views_menu.append_item(self.uif.create_item('View by components', 'app.view-components', ''))
        self.app.add_action(self.uif.create_action("view-components", self.cb.refresh_view, 'components'))

        # Component descriptions view
        views_menu.append_item(self.uif.create_item('View by component description', 'app.view-component-descriptions', ''))
        self.app.add_action(self.uif.create_action("view-component-descriptions", self.cb.refresh_view, 'description'))

        # Bookmarks view
        views_menu.append_item(self.uif.create_item('View bookmarks', 'app.view-bookmarks', ''))
        self.app.add_action(self.uif.create_action("view-bookmarks", self.cb.refresh_view, 'bookmarks'))

        # Category view
        views_menu.append_item(self.uif.create_item('View categories', 'app.view-categories', ''))
        self.app.add_action(self.uif.create_action("view-categories", self.cb.refresh_view, 'category'))

        # Chronologic order view
        views_menu.append_item(self.uif.create_item('View in chronologic order', 'app.chronologic-order', ''))
        self.app.add_action(self.uif.create_action("chronologic-order", self.cb.refresh_view, 'chronologic'))

        # Priority view
        views_menu.append_item(self.uif.create_item('View by priority', 'app.view-priority', ''))
        self.app.add_action(self.uif.create_action("view-priority", self.cb.refresh_view, 'priority'))

        # SAP Note Type view
        views_menu.append_item(self.uif.create_item('View by type', 'app.view-type', ''))
        self.app.add_action(self.uif.create_action("view-type", self.cb.refresh_view, 'type'))

        # Annotations view
        #~ TODO
        #~ views_menu.append_item(self.uif.create_item('View by annotations', 'app.view-annotations', ''))
        #~ self.app.add_action(self.uif.create_action("view-annotations", self.cb_show_dlnotes_window))

        # Set menu model in button
        btnviews = self.gui.get_widget('mnuBtnViews')
        btnviews.set_menu_model(views_menu)


    def setup_menu_settings(self):
        ### SETTINGS POPOVER
        menu = Gio.Menu()
        #~ self.gui.add_widget("menu", menu)
        menu.append_item(self.uif.create_item('Fullscreen', 'app.settings-fullscreen', 'gtk-fullscreen'))
        menu.append_item(self.uif.create_item('Rename current project', 'app.project-rename', 'preferences-desktop-personal'))
        menu.append_item(self.uif.create_item('Refresh current project', 'app.project-refresh', 'view-refresh'))
        menu.append_item(self.uif.create_item('Close current project', 'app.project-close', 'window-close'))
        menu.append_item(self.uif.create_item('Delete current project', 'app.project-delete', 'list-remove'))
        menu.append_item(self.uif.create_item('Export current project', 'app.project-delete', 'document-save-as'))
        window = self.gui.get_window()
        window.set_app_menu(menu)
        app = self.gui.get_app()
        app.add_action(self.uif.create_item("settings-fullscreen"))

        #~ popover_action_group = Gio.SimpleActionGroup()
        btnsettings = self.gui.get_widget("mnuBtnViews")
        popover_settings = Gtk.Popover.new_from_model(btnsettings, menu)
        popover_settings.set_position(Gtk.PositionType.BOTTOM)
        btnsettings.connect('clicked', lambda _: popover_settings.show_all())


    def setup_menus(self):
        self.setup_menu_views()
        #~ self.setup_menu_actions()
        #~ self.setup_menu_settings()


    def show_home_page(self, *args):
        notebook = self.gui.get_widget('notebook')
        notebook.set_current_page(0)


    def show_settings_page(self, *args):
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnoteview.set_view('settings')
        notebook = self.gui.get_widget('notebook')
        notebook.set_current_page(2)


    def show_stats_page(self, *args):
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnoteview.set_view('stats')
        notebook = self.gui.get_widget('notebook')
        notebook.set_current_page(4)


    def show_browser_page(self, *args):
        notebook = self.gui.get_widget('notebook')
        notebook.set_current_page(1)


    def show_search(self, *args):
        revsearch = self.gui.get_widget('revSearch')
        tgbsearch = self.gui.get_widget('tgbSearch')
        if tgbsearch.get_active():
            revsearch.set_reveal_child(True)
            revsearch.set_no_show_all(False)
            revsearch.show_all()
        else:
            revsearch.set_reveal_child(False)
            revsearch.set_no_show_all(True)
            revsearch.hide()


    def hide_props_window(self):
        hpnnotes = self.gui.get_widget('hpnNotesManager')
        boxprops = self.gui.get_widget('boxPropsWidget')
        size = hpnnotes.get_allocation()

        boxprops.set_no_show_all(True)
        boxprops.hide()
        hpnnotes.set_position(size.width)


    def show_props_window(self):
        hpnnotes = self.gui.get_widget('hpnNotesManager')
        boxprops = self.gui.get_widget('boxPropsWidget')
        size = hpnnotes.get_allocation()

        boxprops.set_no_show_all(False)
        boxprops.show_all()
        hpnnotes.show_all()
        hpnnotes.set_position(size.width/5*3)


    def switch_props_window(self, *args):
        tgbprops = self.gui.get_widget('tgbShowManage')

        if tgbprops.get_active():
            self.show_props_window()
        else:
            self.hide_props_window()


    def setup_widgets(self):
        self.mainbox = self.gui.get_widget('mainbox')
        self.mainbox.reparent(self)

        statusbar = self.gui.get_widget('pgbMain')
        statusbar.set_text("")
        statusbar.set_show_text(True)
        statusbar.set_fraction(0.0)
        self.setup_menus()
        #~ self.tasks.setup_widgets()
        notesbox = self.gui.get_widget('notesbox')
        sapnoteview = SAPNoteView(self.controller)
        self.gui.add_widget('sapnoteview', sapnoteview)
        self.gui.add_widget('combobox')
        search = self.gui.add_widget('stySearchInfo')
        #~ search.connect('search_changed', self.search_notes)
        search.connect('activate', self.cb.search_notes)
        self.setup_combobox_search()
        self.swap_widget(notesbox, sapnoteview)


        self.setup_props_window()


        # Buttons
        # Task link button
        self.cb.check_task_link_button_status()

        # button quit
        image = self.gui.get_widget('imgBtnQuit')
        icon = self.im.get_pixbuf_icon('power', 48, 48)
        image.set_from_pixbuf(icon)
        button = self.gui.get_widget('btnQuit')
        button.connect('clicked', self.gui.quit)

        # button about
        image = self.gui.get_widget('imgBtnAbout')
        icon = self.im.get_pixbuf_icon('about', 48, 48)
        image.set_from_pixbuf(icon)
        button = self.gui.get_widget('btnAbout')
        button.connect('clicked', self.uiapp.cb_show_about)

        # button settings
        image = self.gui.get_widget('imgBtnSettings')
        icon = self.im.get_pixbuf_icon('settings', 48, 48)
        image.set_from_pixbuf(icon)
        button = self.gui.get_widget('btnSettings')
        button.connect('clicked', self.show_settings_page)

        # button stats
        image = self.gui.get_widget('imgBtnStats')
        icon = self.im.get_pixbuf_icon('chart', 48, 48)
        image.set_from_pixbuf(icon)
        button = self.gui.get_widget('btnShowStats')
        button.connect('clicked', self.show_stats_page)

        # button show property details
        image = self.gui.get_widget('imgBtnShowProps')
        icon = self.im.get_pixbuf_icon('fingerprint', 48, 48)
        image.set_from_pixbuf(icon)
        button = self.gui.get_widget('btnShowProperties')
        button.connect('clicked', self.cb.show_properties)

        # button show manage window
        image = self.gui.get_widget('imgBtnShowManage')
        icon = self.im.get_pixbuf_icon('subwindow', 48, 48)
        image.set_from_pixbuf(icon)
        button = self.gui.get_widget('tgbShowManage')
        button.connect('toggled', self.switch_props_window)

        # button search
        image = self.gui.get_widget('imgBtnSearch')
        icon = self.im.get_pixbuf_icon('bsearch', 48, 48)
        image.set_from_pixbuf(icon)
        button = self.gui.get_widget('tgbSearch')
        button.connect('toggled', self.show_search)
        revsearch = self.gui.get_widget('revSearch')
        revsearch.hide()
        revsearch.set_no_show_all(True)

        # button import
        image = self.gui.get_widget('imgMnuBtnImport')
        icon = self.im.get_pixbuf_icon('import', 48, 48)
        image.set_from_pixbuf(icon)
        #~ button = self.gui.get_widget('mnuBtnImport')
        #~ button.connect('toggled', self.switch_props_window)

        # button refresh
        image = self.gui.get_widget('imgBtnRefresh')
        icon = self.im.get_pixbuf_icon('refresh', 48, 48)
        image.set_from_pixbuf(icon)
        button = self.gui.get_widget('btnRefreshSAPNoteView')
        button.connect('clicked', self.cb.refresh_and_clear_view)


        button = self.gui.get_widget('btnLinkTasksApply')
        button.connect('clicked', self.cb.link_tasks_to_sapnotes)



        btnaddnote = self.gui.get_widget('btnStartDlNotes')
        btnaddnote.connect('clicked', self.cb.import_notes)



        #~ btnShowAddSAPNotesDlg = self.gui.get_widget('btnShowAddSAPNotesDlg')
        #~ btnShowAddSAPNotesDlg.connect('clicked', self.show_addsapnotes_dialog)

        btnStopDlNotes = self.gui.get_widget('btnStopDlNotes')
        btnStopDlNotes.connect('clicked', self.cb.stop_dl_notes)

        #~ toggle= self.gui.get_widget('tgbFullScreen')
        #~ toggle.connect('toggled', self.uif.fullscreen)
        switch = self.gui.get_widget('schExpandCollapse')
        switch.connect('state-set', sapnoteview.expand_collapse)
        switch = self.gui.get_widget('schSelectNotesAllNone')
        switch.connect('state-set', sapnoteview.select_all_none)


        # Actions button
        button = self.gui.get_widget('mnuBtnActions')

        # Prefs for SAP module
        button = self.gui.add_widget('btnPrefsSAPApply')
        button.connect('clicked', self.cb.apply_preferences)

        button = self.gui.add_widget('btnPrefsSAPCancel')
        button.connect('clicked', self.cb.refresh_view)

        button = self.gui.add_widget('btnPrefsSAPReset')
        button.connect('clicked', self.cb.default_preferences)

        # Notebook Import Widget
        #~ ntbimport = self.gui.add_widget('ntbAddSAPNotes')

        sap_settings = self.prefs.get_custom_settings()
        for setting in sap_settings:
            try:
                widget = self.gui.add_widget(setting)
                widget.set_text(sap_settings[setting])
            except:
                pass


        # Stats
        statsviewer = self.gui.add_widget('scrStatsViewer')

        btnstats = self.gui.add_widget('btnStatsByCompMain')
        btnstats.connect('clicked', self.cb.update_components_stats)
        iconwdg = self.gui.add_widget('imgStatsByCompMain')
        icon = self.im.get_pixbuf_icon('component', 64, 64)
        iconwdg.set_from_pixbuf(icon)

        btnstats = self.gui.add_widget('btnStatsByCategory')
        btnstats.connect('clicked', self.cb.update_categories_stats)
        iconwdg = self.gui.add_widget('imgStatsByCategory')
        icon = self.im.get_pixbuf_icon('category', 64, 64)
        iconwdg.set_from_pixbuf(icon)

        self.hide_props_window()
        self.show_all()
        self.log.debug("GUI loaded")


    def setup_props_window(self):
        imgtitle = self.gui.get_widget('imgPropsTitle')
        icon = self.im.get_icon('fingerprint', 48, 48)
        imgtitle.set_from_pixbuf (icon)
        model = Gtk.TreeStore(str, str)
        trvprops = self.gui.add_widget('trvprops', Gtk.TreeView())
        trvprops.set_model(model)

        #~ ## key
        #~ renderer = Gtk.CellRendererText()
        #~ column = Gtk.TreeViewColumn('Id', renderer, text=0)
        #~ column.set_visible(False)
        #~ column.set_clickable(False)
        #~ column.set_sort_indicator(False)
        #~ trvprops.append_column(column)

        # Property
        renderer = Gtk.CellRendererText()
        renderer.set_alignment(1.0, 0.5)
        column = Gtk.TreeViewColumn('Property', renderer, markup=0)
        column.set_visible(True)
        column.set_expand(False)
        column.set_clickable(True)
        column.set_sort_indicator(True)
        trvprops.append_column(column)

        # Value
        renderer = Gtk.CellRendererText()
        renderer.set_alignment(0.0, 0.5)
        column = Gtk.TreeViewColumn('Value', renderer, markup=1)
        column.set_visible(True)
        column.set_expand(True)
        column.set_clickable(True)
        column.set_sort_indicator(True)
        trvprops.append_column(column)
        trvprops.show_all()

        trvprops.set_headers_visible(True)
        trvprops.set_enable_search(True)
        trvprops.set_grid_lines(Gtk.TreeViewGridLines.NONE)
        trvprops.set_search_column(1)
        #~ trvprops.connect('row-activated', self.double_click)
        selection = trvprops.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        #~ trvprops.set_search_entry(self.pname)

        container = self.gui.get_widget('boxProps')
        self.gui.swap_widget(container, trvprops)

    def set_notes_manager_pane_position(self, pane, rectangle):
        pass
        #~ self.log.debug(type(pane.get_allocation()))
        position = rectangle.width/5*3
        pane.set_position(position)
        self.log.debug("Pane position: %s" % position)



    def __completion_func(self, completion, key, iter):
        model = completion.get_model()
        text = model.get_value(iter, 0)
        if key.upper() in text.upper():
            return True
        return False


    def setup_combobox_completions(self, key):
        model = Gtk.ListStore(str)
        search = self.gui.get_widget("stySearchInfo")
        completion = Gtk.EntryCompletion()
        completion.set_model(model)
        completion.set_text_column(0)
        completion.set_match_func(self.__completion_func)
        search.set_completion(completion)

        stats = self.db.get_stats()

        try:
            items = list(stats[key])
            items.sort()
            for item in items:
                model.append([item])
        except:
            pass


    def cb_combobox_changed(self, combobox):
        model = combobox.get_model()
        treeiter = combobox.get_active_iter()
        key = model[treeiter][0]
        self.gui.set_key('cmbvalue', key)
        self.setup_combobox_completions(key)


    def setup_combobox_search(self):
        combobox = self.gui.get_widget('cmbSearchInfo')
        model = Gtk.TreeStore(str, str)
        combobox.set_model(model)

        ## key
        cell = Gtk.CellRendererText()
        cell.set_visible(False)
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 0)

        ## value
        cell = Gtk.CellRendererText()
        cell.set_alignment(0.0, 0.5)
        combobox.pack_start(cell, expand=False)
        combobox.add_attribute(cell, 'markup', 1)
        combobox.connect('changed', self.cb_combobox_changed)

        model.append(None, ['search', 'Search in all database'])
        model.append(None, ['project', 'Filter by project name'])
        model.append(None, ['task', 'Filter by task name'])
        model.append(None, ['component', 'Filter by component'])
        model.append(None, ['category', 'Filter by category'])
        model.append(None, ['type', 'Filter by type'])
        model.append(None, ['id', 'Filter by Id'])
        model.append(None, ['title', 'Filter by title'])
        model.append(None, ['priority', 'Filter by priority'])
        model.append(None, ['version', 'Filter by version'])
        #~ model.append(None, ['released', 'Filter by release date'])

        combobox.set_active(0)


    def get_services(self):
        """Load services to be used in this class
        """
        self.gui = self.controller.get_service("GUI")
        self.app = self.gui.get_app()
        LOG_FILE = self.controller.get_file('LOG')
        self.log = get_logger('GtkAppWindow', LOG_FILE)
        self.db = self.controller.get_service("DB")
        self.uif = self.controller.get_service("UIF")
        self.prefs = self.controller.get_service("Settings")
        self.im = self.controller.get_service('IM')
        self.cb = self.controller.get_service('Callbacks')
        self.tasks = self.controller.get_service('Tasks')


    def swap_widget(self, container, combobox):
        """Shortcut to GUI.swap_widget method
        """
        self.gui.swap_widget(container, combobox)
