#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: tasks.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Tasks service

import os
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Pango
from datetime import datetime
from dateutil import parser as dateparser

from .service import Service


class Tasks(Service):
    def initialize(self):
        self.get_services()
        self.setup_widgets()
        self.__init_tasks_store()
        self.load_tasks()


    def __init_tasks_store(self):
        TASKS_FILE = self.get_file('TASKS')
        if not os.path.exists(TASKS_FILE):
            self.log.info("Creating store for tasks: %s" % TASKS_FILE)
            ftasks = open(TASKS_FILE, 'w')
            ftasks.close()


    def setup_widgets(self):
        # setup widgets
        self.window = self.gui.add_widget('boxProps')
        self.pname = self.gui.add_widget('etyTaskName')
        self.pname.connect('activate', self.add_task)
        self.boxtask = self.gui.add_widget('boxTasks')
        self.btnadd = self.gui.add_widget('btnAddTask')
        self.btnadd.connect('clicked', self.add_task)
        self.btndel = self.gui.add_widget('btnDelTask')
        self.btndel.connect('clicked', self.delete_task)
        self.treeview = Gtk.TreeView()
        self.gui.add_widget('trvtaskwin', self.treeview)
        self.gui.add_widget('boxAcceptCancelTasks')
        self.boxtask.add(self.treeview)

        # setup model
        model = Gtk.ListStore(
            bool,           # CheckBox
            str             # Task name
        )
        self.treeview.set_model(model)

        # setup columns
        # Checkbox
        renderer = Gtk.CellRendererToggle()
        renderer.connect("toggled", self.on_cell_toggled)
        column = Gtk.TreeViewColumn('', renderer, active=0)
        column.set_visible(True)
        column.set_expand(False)
        column.set_clickable(False)
        column.set_sort_indicator(False)
        self.treeview.append_column(column)

        # Task name
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Task name', renderer, text=1)
        column.set_visible(True)
        column.set_sort_column_id(1)
        column.set_expand(True)
        column.set_clickable(True)
        column.set_sort_indicator(True)
        self.treeview.append_column(column)

        # Filters
        #Creating the filter, feeding it with the liststore model
        #~ self.task_filter = model.filter_new()
        #setting the filter function, note that we're not using the
        #~ self.task_filter.set_visible_func(self.task_filter_func)
        #~ self.task_filter.set_visible_column(1)

        # Treeview features
        self.treeview.set_headers_visible(True)
        self.treeview.set_enable_search(True)
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.NONE)
        self.treeview.set_search_column(1)
        self.treeview.connect('row-activated', self.double_click)
        selection = self.treeview.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.treeview.set_search_entry(self.pname)


    def clear(self):
        model = self.treeview.get_model()
        model.clear()


    def set_model(self, model):
        self.treeview.set_model(model)


    # row task visibility
    def task_row_visibility(self, model, iter, data):
        entry = self.gui.get_widget('etyTaskName')
        text = entry.get_text()

        return text.upper() in model.get_value(iter, 1)


    def task_filter_func(self, model, iter, data):
        """Tests if the task in the row is the one in the filter"""
        entry = self.gui.get_widget('etyTaskName')
        task = entry.get_text()
        task_row = model[iter][1]

        if task.upper() in task_row.upper():
            return True
        else:
            return False


    def delete_task(self, *args):
        db = self.app.get_service('DB')
        found = 0
        selection = self.treeview.get_selection()
        result = selection.get_selected()
        if result: #result could be None
            model, iter = result
            task = model.get_value(iter, 1)
            sapnotes = db.get_notes()
            for sapnote in sapnotes:
                try:
                    tasks = sapnotes[sapnote]['tasks']
                    if task in tasks:
                        found += 1
                except:
                    pass
            if found > 1:
                self.log.warning("Task %s is still assigned to other SAP Notes" % task)
                head = "Task could not be deleted"
                body = "Task %s is still assigned to other SAP Notes" % task
                self.uif.message_dialog(head , body)
            else:
                model.remove(iter)
                self.log.info("Task deleted: %s" % task)
                self.save_tasks()



    def add_task(self, *args):
        task = self.pname.get_text()
        model = self.treeview.get_model()

        found = False
        for row in model:
            if row[1].upper() == task.upper():
                self.log.info("Task already exists: %s" % task)
                found = True

        if not found and len(task) > 0:
            model.append([False, task])
            self.log.info("Task added: %s" % task)

        self.pname.set_text('')
        self.save_tasks()
        self.load_tasks()



    def show_window(self, sapnotes=[], active=None):
        ntboperations = self.gui.get_widget('ntbOperations')
        ntboperations.set_current_page(1)
        winoper = self.gui.get_widget('tgbShowManage')
        switch = winoper.get_active()
        if active is None:
            if switch is True:
                active = True
            else:
                active = False
        winoper.set_active(active)
        self.load_tasks(sapnotes)


    def get_services(self):
        self.gui = self.app.get_service("GUI")
        self.sap = self.app.get_service('SAP')
        self.uif = self.app.get_service('UIF')
        self.cb = self.app.get_service('Callbacks')
        self.db = self.app.get_service('DB')


    def double_click(self, treeview, row, col):
        model = treeview.get_model()
        self.pname.set_text(model[row][1])


    def populate(self, sapnotes):
        model = self.treeview.get_model()
        model.clear()
        #~ model.append([bool, str])


    def changed(self, *args):
        try:
            model, treeiters = self.selection.get_selected_rows()
            selected = set()
            if len(treeiters) > 0:
                for treeiter in treeiters:
                    if treeiter != None:
                        selected.add(model[treeiter][0])
            print (selected)

        except Exception as error:
            self.log.error (self.get_traceback())


    def select(self, tasks):
        model = self.treeview.get_model()

        def select_task(model, path, iter, user_data=None):
            task = model.get_value(iter, 1)
            if task in tasks:
                model[path][0] = True
                self.log.debug("Task '%s' switch to true" % task)
            else:
                model[path][0] = False
            return False

        model.foreach(select_task)


    def on_cell_toggled(self, widget, path):
        cb = self.get_service('Callbacks')
        model = self.treeview.get_model()
        model[path][0] = not model[path][0]
        cb.check_task_link_button_status()
        #~ button = self.gui.get_widget('btnLinkTasksApply')
        #~ sapnoteview = self.gui.get_widget('sapnoteview')

        #~ tasks_selected = len(self.get_selected()) > 0
        #~ notes_selected = len(sapnoteview.get_selected_notes()) > 0
        #~ if  tasks_selected and notes_selected:
            #~ button.set_no_show_all(False)
            #~ button.show_all()
        #~ else:
            #~ button.hide()
            #~ button.set_no_show_all(True)



    def get_selected(self):
        model = self.treeview.get_model()
        tasks = set()

        def traverse_treeview(model, path, iter, user_data=None):
            toggled = model.get_value(iter, 0)
            if toggled:
                task = model.get_value(iter, 1)
                tasks.add(task)
            return False

        model.foreach(traverse_treeview)
        ltasks = list(tasks)
        ltasks.sort()

        #~ self.log.debug("Tasks selected: %s" % ', '.join(tasks))
        return ltasks


    #~ def get_selected_notes(self):
        #~ sapnoteview = self.gui.get_widget('sapnoteview')
        #~ return sapnoteview.get_selected_notes()


    def link_to_task(self, *args):
        sapnoteview = self.gui.get_widget('sapnoteview')

        self.save_tasks()
        sapnotes = list(sapnoteview.get_selected_notes())
        model = self.treeview.get_model()
        tasks = []
        for row in model:
           link = row[0]
           if link == True:
                tasks.append(row[1])

        sapnotes.sort()
        tasks.sort()
        self.sap.link_to_task(sapnotes, tasks)
        self.cb.refresh_view(view='tasks')


    def get_all_tasks(self):
        tasks = []
        model = self.treeview.get_model()
        for row in model:
            tasks.append(row[1])
        tasks.sort()

        return tasks


    def load_tasks(self, sapnotes=[]):
        model = self.treeview.get_model()
        TASKS_FILE = self.get_file('TASKS')
        alltasks = open(TASKS_FILE, 'r').readlines()
        model.clear()
        alltasks.sort()
        for task in alltasks:
            model.append([False, task[0:-1]])


    def save_tasks(self):
        TASKS_FILE = self.get_file('TASKS')
        tasks = self.get_all_tasks()

        ftasks = open(TASKS_FILE, 'w')
        for task in tasks:
            ftasks.write("%s\n" % task)
            self.log.info("Task saved: %s" % task)
        ftasks.close()



    def save_tasks_from_stats(self, alltasks):
        settings = {}
        tasks = ','.join(alltasks)
        settings['Tasks'] = tasks
        self.config[self.section] = settings
        self.save_config()
