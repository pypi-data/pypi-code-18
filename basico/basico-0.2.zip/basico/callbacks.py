#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: callbacks.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: UI and related callbacks service

import os
import csv
import json
import time
import glob
from os.path import basename
from datetime import datetime

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Pango
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import WebKit

from concurrent.futures import ThreadPoolExecutor as Executor

from .service import Service

SEP = os.path.sep

# PROPKEYS = CSV headers. SAP Note metadata
PROPKEYS = ['id', 'title', 'type', 'componentkey',
            'componenttxt', 'category', 'priority', 'releaseon',
            'language', 'version']

# Extend PROPKEYS with custom basico metadata
PROPKEYS.extend (['Tasks', 'Bookmark'])

class Callback(Service):
    def initialize(self):
        self.get_services()

    def get_services(self):
        self.gui = self.app.get_service('GUI')
        self.uif = self.app.get_service("UIF")
        self.sap = self.app.get_service('SAP')
        self.tasks = self.app.get_service('Tasks')
        self.alert = self.app.get_service('Notify')
        #~ self.stats = self.app.get_service('Stats')
        self.utils = self.app.get_service('Utils')

    def execute_action(self, *args):
        action = args[0]
        action_name = action.get_name()
        try:
            callback = "self.%s()" % action_name.replace('-', '_')
            return eval(callback)
        except Exception as error:
            self.log.error(error)
            self.log.error("Callback for action '%s' not registered" % action_name)
            raise


    def actions_browse(self, *args):
        SAP_NOTE_URL = self.sap.get_config_value('CNF_SAP_NOTE_URL')
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = sapnoteview.get_selected_notes()
        lurl = []
        for sid in sapnotes:
            url = SAP_NOTE_URL % sid
            lurl.append(url)
            self.log.debug("Browsing SAP Note %s" % sid)
        self.utils.browse(lurl)


    def actions_other_delete(self, *args):
        db = self.get_service('DB')
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = sapnoteview.get_selected_notes()
        sapnotes.sort()
        winroot = self.gui.get_widget('mainwinow')

        dialog = Gtk.MessageDialog(winroot, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, "Are you sure?")
        dialog.set_title("Deleting SAP Notes...")
        dialog.set_modal(True)
        dialog.set_transient_for(winroot)
        dialog.format_secondary_text(
            "These SAP Notes will be deleted:\n%s" % ', '.join(sapnotes))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            db = self.get_service('DB')
            sapnotes = sapnoteview.get_selected_notes()
            for sapnote in sapnotes:
                db.delete(sapnote)
            self.search_notes()
            self.refresh_view()
            self.alert.show('Delete', 'Selected SAP Notes deleted', 'information')
            self.log.info("Selected SAP Notes deleted")
            db.save_notes()
        elif response == Gtk.ResponseType.CANCEL:
            self.alert.show('Delete', 'Delete action canceled by user', 'warning')
            self.log.info("Delete action canceled by user")

        dialog.destroy()

        return response


    def show_properties(self, *args):
        notebook = self.gui.get_widget('ntbOperations')
        toggle = self.gui.get_widget('tgbShowManage')
        notebook.set_current_page(0)
        toggle.set_active(True)


    def actions_manage_tasks(self, *args):
        #~ sapnoteview = self.gui.get_widget('sapnoteview')
        #~ try:
            #~ sapnotes = sapnoteview.get_selected_notes()
        #~ except:
            #~ sapnote = ''
        self.tasks.show_window(active=True)


    def link_tasks_to_sapnotes(self, *args):
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = sapnoteview.get_selected_notes()
        tasks = self.tasks.get_selected()
        self.sap.link_to_task(sapnotes, tasks)

    def actions_bookmark(self, *args):
        db = self.get_service('DB')
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = sapnoteview.get_selected_notes()
        self.log.debug("Action bookmark triggered for SAP Notes: %s" % sapnotes)
        view = sapnoteview.get_view()
        self.sap.set_bookmark(sapnotes)
        db.save_notes()
        self.refresh_view(view=view)
        self.alert.show('Bookmarks', 'Selected SAP Notes bookmarked', 'information')


    def actions_unbookmark(self, *args):
        db = self.get_service('DB')
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = sapnoteview.get_selected_notes()
        self.log.debug("Action unbookmark triggered for SAP Notes: %s" % sapnotes)
        self.sap.set_no_bookmark(sapnotes)
        db.save_notes()
        self.refresh_view(view='bookmarks')
        self.alert.show('Bookmarks', 'Selected SAP Notes unbookmarked', 'information')


    def actions_export_csv(self, *args):
        db = self.get_service('DB')
        rootwin = self.gui.get_widget('mainwndow')
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = sapnoteview.get_selected_notes()
        dialog = Gtk.FileChooserDialog("Save file", rootwin,
            Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            export_path = dialog.get_filename()
            writer = csv.writer(open(export_path, 'w'), delimiter=';', quoting=csv.QUOTE_ALL)
            csvrow = []

            for key in PROPKEYS:
                csvrow.append(key.capitalize())
            writer.writerow(csvrow)

            for tid in sapnotes:
                sid = "0"*(10 - len(tid)) + tid
                self.log.debug("Exporting SAP Note %s to CSV file" % sid)
                csvrow = []
                props = db.get_sapnote_metadata(sid)

                for prop in PROPKEYS:
                    if prop == 'tasks':
                        tasks = ', '.join(props[prop])
                        csvrow.append(tasks)
                    else:
                        csvrow.append(props[prop])
                writer.writerow(csvrow)
            self.alert.show('Export', 'Selected SAP Notes exported successfully to CSV format', 'information')
            self.log.info("Selected SAP Notes exported to CSV format: %s" % export_path)
        else:
            self.alert.show('Export', 'Export canceled by user', 'warning')
            self.log.info("Export canceled by user")
        dialog.destroy()


    def actions_export_txt(self, *args):
        rootwin = self.gui.get_widget('mainwndow')
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = sapnoteview.get_selected_notes()
        dialog = Gtk.FileChooserDialog("Save file", rootwin,
            Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            export_path = dialog.get_filename()
            fout = open(export_path, 'w')
            for sapnote in sapnotes:
                fout.write("%s\n" % sapnote)
            self.alert.show('Export', 'Selected SAP Notes exported successfully to TXT format', 'information')
            self.log.info("Selected SAP Notes exported to TXT format: %s" % export_path)
        else:
            self.alert.show('Export', 'Export canceled by user', 'warning')
            self.log.info("Export canceled by user")
        dialog.destroy()


    def actions_export_json(self, *args):
        db = self.get_service('DB')
        rootwin = self.gui.get_widget('mainwndow')
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = sapnoteview.get_selected_notes()
        dialog = Gtk.FileChooserDialog("Save file", rootwin,
            Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            export_path = dialog.get_filename()
            bag = {}
            for tid in sapnotes:
                sid = "0"*(10 - len(tid)) + tid
                sapnote = db.get_sapnote_metadata(sid)
                bag[sid] = sapnote
            now = datetime.now()
            target = export_path + SEP + 'basico-%s.json' % now.strftime("%Y%m%d_%H%M%S")
            db.export_basico_package(bag, target)
            self.alert.show('Export', 'Selected SAP Notes exported successfully to JSON format', 'information')
            self.log.info("Selected SAP Notes exported to JSON: %s" % target)
        else:
            self.alert.show('Export', 'Export canceled by user', 'warning')
            self.log.info("Export canceled by user")
        dialog.destroy()


    def actions_import_json(self, *args):
        self.import_notes_from_file()
        #~ db = self.get_service('DB')
        #~ rootwin = self.gui.get_widget('mainwndow')
        #~ sapnoteview = self.gui.get_widget('sapnoteview')
        #~ sapnotes = sapnoteview.get_selected_notes()
        #~ dialog = Gtk.FileChooserDialog("Select Basico JSON file", rootwin,
            #~ Gtk.FileChooserAction.OPEN,
                #~ (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 #~ Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        #~ response = dialog.run()

        #~ if response == Gtk.ResponseType.OK:
            #~ source = dialog.get_filename()
            #~ try:
                #~ with open(source, 'r') as fp:
                    #~ bag = json.load(fp)
                    #~ db.import(bag)
                    #~ self.log.debug ("Imported %d notes" % len(bag))
            #~ except Exception as error:
                #~ self.log.info("SAP Notes database not found. Creating a new one")
                #~ self.save_notes()

            #~ self.alert.show('Export', 'Selected SAP Notes exported successfully to JSON format', 'information')
            #~ self.log.info("Selected SAP Notes exported to JSON: %s" % target)
        #~ else:
            #~ self.alert.show('Export', 'Export canceled by user', 'warning')
            #~ self.log.info("Export canceled by user")
        #~ dialog.destroy()



    def actions_import_launchpad(self, *args):
        self.show_addsapnotes_dialog()


    def set_search_filter_key(self, key):
        self.gui.set_key('cmbvalue', key)


    def get_search_filter_key(self):
        cmbvalue = self.gui.get_key('cmbvalue')


    def set_search_term(self, term):
        searchentry = self.gui.get_widget("stySearchInfo")
        searchentry.set_text(term)


    def search_notes(self, *args):
        db = self.get_service('DB')
        searchentry = self.gui.get_widget("stySearchInfo")
        cmbvalue = self.gui.get_key('cmbvalue')
        self.log.debug("Serch term: %s" % cmbvalue)
        try:
            term = searchentry.get_text()
        except:
            term = ''

        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnotes = db.get_notes()
        found = {}

        if len(term) == 0:
            self.current_notes = found = sapnotes
            sapnoteview.populate(found)
            sapnoteview.collapse()
            self.log.debug("Displaying all database")
            return

        self.log.debug("Looking for '%s'" % term)
        if cmbvalue == 'search':
            for sid in sapnotes:
                if term.upper() in sapnotes[sid]['title'].upper():
                   found[sid] = sapnotes[sid]
        elif cmbvalue == 'project':
            for sid in sapnotes:
                try:
                    projects = sapnotes[sid]['projects']
                    for project in projects:
                        if term.upper() in project.upper():
                           found[sid] = sapnotes[sid]
                except: pass
        elif cmbvalue == 'task':
            for sid in sapnotes:
                try:
                    tasks = sapnotes[sid]['tasks']
                    for task in tasks:
                        if term.upper() in task.upper():
                           found[sid] = sapnotes[sid]
                except: pass
        elif cmbvalue == 'title':
            for sid in sapnotes:
                try:
                    title = sapnotes[sid]['title']
                    if term.upper() in title.upper():
                       found[sid] = sapnotes[sid]
                except: pass
        elif cmbvalue == 'priority':
            for sid in sapnotes:
                try:
                    priority = sapnotes[sid]['priority']
                    if term.upper() in priority.upper():
                       found[sid] = sapnotes[sid]
                except: pass
        elif cmbvalue == 'component':
            for sid in sapnotes:
                if term.upper() in sapnotes[sid]['componentkey'].upper():
                   found[sid] = sapnotes[sid]
        elif cmbvalue == 'category':
            for sid in sapnotes:
                if term.upper() in sapnotes[sid]['category'].upper():
                   found[sid] = sapnotes[sid]
        elif cmbvalue == 'type':
            for sid in sapnotes:
                if term.upper() in sapnotes[sid]['type'].upper():
                   found[sid] = sapnotes[sid]
        elif cmbvalue == 'version':
            for sid in sapnotes:
                if term.upper() in sapnotes[sid]['version'].upper():
                   found[sid] = sapnotes[sid]
        elif cmbvalue == 'id':
            for sid in sapnotes:
                if term in sid:
                   found[sid] = sapnotes[sid]
        self.log.info("Term: '%s' (%d results)" % (term, len(found)))
        self.current_notes = found
        self.log.debug("Current Notes: %d" % len(self.current_notes))
        sapnoteview.populate(found)


    #~ def import_notes(self, entry):
        #~ ntbimport = self.gui.get_widget('ntbAddSAPNotes')
        #~ imptype = ntbimport.get_current_page() # 0 -> Download, 1 -> Import from file
        #~ if imptype == 0:
            #~ self.import_notes_from_sapnet()
        #~ elif imptype == 1:
            #~ self.import_notes_from_file()

    def import_notes(self, entry):
        self.import_notes_from_sapnet()


    def import_notes_from_file(self):
        db = self.get_service('DB')
        notebook = self.gui.get_widget('notebook')
        rootwin = self.gui.get_widget('mainwinow')

        dialog = Gtk.FileChooserDialog("Select Basico JSON file", rootwin,
            Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            source = dialog.get_filename()
            try:
                with open(source, 'r') as fp:
                    bag = json.load(fp)
                    db.import_sapnotes(bag)
                    self.log.info ("Imported %d notes from %s" % (len(bag), source))
            except Exception as error:
                self.log.info("SAP Notes database not found. Creating a new one")
                self.save_notes()
            sapnoteview = self.gui.get_widget('sapnoteview')
            self.current_notes = bag
            sapnoteview.populate(bag)
            db.save_notes()
            self.refresh_view()
            switch = self.gui.get_widget('schSelectNotesAllNone')
            sapnoteview.select_all_none(switch, True)
            sapnoteview.select_all_none(switch, False)
            sapnoteview.expand_all()
        else:
            self.alert.show('Import', 'Nothing imported', 'error')
            self.log.debug("Nothing imported")
        dialog.destroy()

    def import_notes_from_sapnet(self):
        db = self.get_service('DB')
        driver = self.get_service('Driver')

        notebook = self.gui.get_widget('notebook')
        winroot = self.gui.get_widget('mainwinow')
        sapnotes = []
        bag = set()
        txtnotes = self.gui.get_widget('txtSAPNotes')
        textbuffer = txtnotes.get_buffer()
        istart, iend = textbuffer.get_bounds()
        lines = textbuffer.get_text(istart, iend, False)

        lines = lines.replace(' ', ',')
        lines = lines.replace('\n', ',')
        sapnotes.extend(lines.split(','))

        for sapnote in sapnotes:
            if len(sapnote.strip()) > 0:
                bag.add(sapnote.strip())

        self.log.debug("%d SAP Notes to be downloaded: %s" % (len(bag), ', '.join(list(bag))))

        resnotes = {}

        self.sap.start_fetching(len(bag))
        dlbag = {}

        # FIXME: max_workers = 1 = Threads disabled
        with Executor(max_workers=1) as exe:
            jobs = []
            for sapnote in bag:
                job = exe.submit(self.sap.fetch, sapnote)
                jobs.append(job)

            for job in jobs:
                rc, sapnote = job.result()
                self.log.debug("\tRC SAP Note %s: %s" % (sapnote, rc))
                resnotes[sapnote] = rc
                time.sleep(0.1)

        driver.close()
        self.sap.stop_fetching()
        db.save_notes()
        db.build_stats()

        textbuffer.set_text("")
        self.log.info("Task completed.")
        notebook.set_current_page(0)
        dialog = Gtk.MessageDialog(winroot, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Task completed")
        msgrc = ""
        ko = 0
        ok = 0
        for sapnote in resnotes:
            rc = resnotes[sapnote]
            if rc:
                ok += 1
            else:
                ko += 1
        msgrc += "Downloaded: %d\nErroneus: %d" % (ok, ko)
        self.alert.show('Download', msgrc, 'information')
        dlbag = {}
        mysapnotes = db.get_notes()
        erroneus = set()
        for sid in bag:
            sid = "0"*(10 - len(sid)) + sid
            try:
                dlbag[sid] = mysapnotes[sid]
            except Exception as error:
                self.log.error(error)
                erroneus.add(sid)

        sapnoteview = self.gui.get_widget('sapnoteview')
        self.current_notes = dlbag
        #~ self.refresh_view()
        self.refresh_and_clear_view()
        sapnoteview.populate(dlbag)
        sapnoteview.expand_all()
        boxMenu = self.gui.get_widget('boxMenu')
        boxMenu.show_all()


    def stop_dl_notes(self, *args):
        notebook = self.gui.get_widget('notebook')
        txtSAPNotes = self.gui.get_widget('txtSAPNotes')
        buffer = txtSAPNotes.get_buffer()
        buffer.set_text("")
        notebook.set_current_page(0)
        self.refresh_view()
        #~ self.alert.show('Download', 'Action canceled by user', 'warning')
        boxMenu = self.gui.get_widget('boxMenu')
        boxMenu.show_all()
        self.refresh_and_clear_view()


    def rebuild_database(self, *args):
        self.log.debug("Rebuild database...")

        db = self.get_service('DB')
        DB_DIR = self.get_var('DB', 'local')

        #~ FSAPNOTE = DB_DIR + sid + '.xml'
        #~ if path is None:
            #~ path = DB_DIR

        files = glob.glob("%s%s*.xml" % (DB_DIR, SEP))
        sap = self.app.get_service('SAP')
        for filename in files:
            self.log.debug("Filename: %s" % filename)
            sid = basename(filename)[0:-4]
            self.log.debug("SAP Note Id: %s" % sid)

            valid = False
            if db.is_stored(sid):
                self.log.debug("\tSAP Note %s will be analyzed again" % sid)
                content = db.get_sapnote_content(sid)
                sapnote = sap.analyze_sapnote_metadata(sid, content)
                if len(sapnote) > 0:
                    db = self.get_service('DB')
                    db.add(sapnote)
                    db.store(sid, content)
                    valid = True

        self.refresh_view()

    def refresh_and_clear_view(self, *args):
        switch = self.gui.get_widget('schSelectNotesAllNone')
        sapnoteview = self.gui.get_widget('sapnoteview')
        self.set_search_filter_key('search')
        self.set_search_term('')
        self.search_notes()
        self.refresh_view()
        sapnoteview.select_all_none(switch, False)
        sapnoteview.collapse()


    def refresh_view(self, action=None, callback=None, view=None):
        window = self.gui.get_widget('mainwindow')
        sapnoteview = self.gui.get_widget('sapnoteview')
        switch_expand = self.gui.get_widget('schExpandCollapse')
        switch_select = self.gui.get_widget('schSelectNotesAllNone')
        #~ active_ = switch.get_active()

        if view is not None:
            viewlabel = self.gui.get_widget('lblViewCurrent')
            name = "<span size='20000'><b>%-10s</b></span>" % view.capitalize()
            viewlabel.set_markup(name)
        sapnoteview.set_view(view)
        self.search_notes()
        switch_expand.set_active(True)
        switch_expand.set_active(False)
        switch_select.set_active(False)
        switch_select.set_active(True)
        switch_select.set_active(False)
        window.show_home_page()


    def setup_menu_import(self):
        sapnoteview = self.gui.get_widget('sapnoteview')
        view = sapnoteview.get_view()

        ### ACTIONS POPOVER
        app = self.gui.get_app()

        ## Action Menu
        actions_menu = Gio.Menu()

        # Import submenu
        #~ actions_import_submenu = Gio.Menu()
        # Import Basico Package
        actions_menu.append_item(self.uif.create_item('Import Basico Package', 'app.actions-import-basico', 'document-open'))
        #~ app.add_action(self.uif.create_action("actions-import-basico"))

        # Import from JSON file
        actions_menu.append_item(self.uif.create_item('Import JSON file', 'app.actions-import-json', 'document-open'))
        app.add_action(self.uif.create_action("actions-import-json"))

        #~ Import from SAP Launchpad
        actions_menu.append_item(self.uif.create_item('Import SAP Notes from SAP Launchpad', 'app.actions-import-launchpad', 'download'))
        app.add_action(self.uif.create_action("actions-import-launchpad"))

        #~ actions_menu.append_submenu('Import', actions_import_submenu)

        # MnuButton valid with any modern version of Gtk (?> 3.10)
        btnactions = self.gui.get_widget('mnuBtnImport')
        btnactions.set_always_show_image(True)
        btnactions.set_property("use-popover", True)
        btnactions.set_menu_model(actions_menu)


    def setup_menu_actions(self):
        sapnoteview = self.gui.get_widget('sapnoteview')
        view = sapnoteview.get_view()

        ### ACTIONS POPOVER
        app = self.gui.get_app()

        ## Action Menu
        actions_menu = Gio.Menu()

        #~ # Browse SAP Notes
        actions_menu.append_item(self.uif.create_item('Browse SAP Note(s)', 'app.actions-browse', 'browse'))
        app.add_action(self.uif.create_action("actions-browse"))

        if view == 'bookmarks':
            #~ Unbookmark SAP Note(s) items
            actions_menu.append_item(self.uif.create_item('Unbookmark SAP Note(s)', 'app.actions-unbookmark', 'bookmark'))
            app.add_action(self.uif.create_action("actions-unbookmark"))
        else:
            #~ Bookmark SAP Note(s) items
            actions_menu.append_item(self.uif.create_item('Bookmark SAP Note(s)', 'app.actions-bookmark', 'bookmark'))
            app.add_action(self.uif.create_action("actions-bookmark"))

        # Manage task
        actions_menu.append_item(self.uif.create_item('Manage tasks', 'app.actions-manage-tasks', 'tasks'))
        app.add_action(self.uif.create_action("actions-manage-tasks"))

        # Export submenu
        actions_export_submenu = Gio.Menu()

        #~ Export to JSON
        actions_export_submenu.append_item(self.uif.create_item('Export as JSON', 'app.actions-export-json', 'document-save'))
        app.add_action(self.uif.create_action("actions-export-json"))
        #~ Export to CSV
        actions_export_submenu.append_item(self.uif.create_item('Export as CSV', 'app.actions-export-csv', 'document-save'))
        app.add_action(self.uif.create_action("actions-export-csv"))
        #~ Export to TXT
        actions_export_submenu.append_item(self.uif.create_item('Export to plaint text', 'app.actions-export-txt', 'document-save'))
        app.add_action(self.uif.create_action("actions-export-txt"))
        #~ Export to BCO
        #~ actions_export_submenu.append_item(self.uif.create_item('Export as Basico Package Object (BCO)', 'app.actions-export-bco', 'document-save'))
        #~ app.add_action(self.uif.create_action("actions-export-bco"))
        actions_menu.append_submenu('Export', actions_export_submenu)
        #~ actions_menu.append_section('Export', actions_export_submenu)

        # Refresh SAP Notes
        #~ actions_menu.append_item(self.uif.create_item('Refresh selected SAP Notes', 'app.actions-other-refresh', 'refresh'))
        #~ app.add_action(self.uif.create_action("actions-other-refresh"))

        # Delete SAP Notes
        actions_menu.append_item(self.uif.create_item('Delete selected SAP Notes', 'app.actions-other-delete', 'delete'))
        app.add_action(self.uif.create_action("actions-other-delete"))

        # MnuButton valid with any modern version of Gtk (?> 3.10)
        btnactions = self.gui.get_widget('mnuBtnActions')
        btnactions.set_always_show_image(True)
        btnactions.set_property("use-popover", True)
        btnactions.set_menu_model(actions_menu)


    def show_addsapnotes_dialog(self, *args):
        sapnoteview = self.gui.get_widget('sapnoteview')
        sapnoteview.set_view('download')
        notebook = self.gui.get_widget('notebook')
        boxMenu = self.gui.get_widget('boxMenu')
        boxMenu.hide()
        notebook.set_current_page(1)


    def default_preferences(self, *args):
        prefs = self.get_service('Settings')
        gui = self.get_service('GUI')
        settings = prefs.get_default_settings()
        for key in settings:
            widget = gui.get_widget(key)
            widget.set_text(str(settings[key]))

        self.config[self.section] = settings
        self.save_config()
        self.log.debug("Settings reverted to default")


    def apply_preferences(self, *args):
        self.sap.apply_preferences()
        notebook = self.gui.get_widget('notebook')
        notebook.set_current_page(0)
        self.refresh_view(view='tasks')
        self.alert.show('Settings', 'SAP preferences saved', 'information')


    def update_components_stats(self, *args):
        statsviewer = self.gui.get_widget('scrStatsViewer')
        view = WebKit.WebView()
        chart = self.stats.build_pie_maincomp()
        view.load_string(chart, 'text/html', 'UTF-8','/')
        self.gui.swap_widget(statsviewer, view)


    def update_categories_stats(self, *args):
        statsviewer = self.gui.get_widget('scrStatsViewer')
        view = WebKit.WebView()
        chart = self.stats.build_pie_categories()
        view.load_string(chart, 'text/html', 'UTF-8','/')
        self.gui.swap_widget(statsviewer, view)


    def check_task_link_button_status(self):
        tasks = self.get_service('Tasks')
        button = self.gui.get_widget('btnLinkTasksApply')
        sapnoteview = self.gui.get_widget('sapnoteview')

        tasks_selected = len(tasks.get_selected()) > 0
        notes_selected = len(sapnoteview.get_selected_notes()) > 0
        if  tasks_selected and notes_selected:
            #~ button.set_no_show_all(False)
            #~ button.show_all()
            button.set_sensitive(True)
            self.log.debug("Task link button enabled")
        else:
            #~ button.hide()
            #~ button.set_no_show_all(True)
            button.set_sensitive(False)
            self.log.debug("Task link button disabled")


    def test(self, *args):
        self.log.debug(args)


