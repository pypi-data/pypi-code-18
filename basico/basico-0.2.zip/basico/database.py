#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: database.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Database service

import os
from os.path import basename
#~ import sys
#~ import time
import json
import glob
#~ import shutil
#~ import traceback
#~ from shutil import which
from cgi import escape

from .env import LPATH
from .service import Service

SEP = os.path.sep

class Database(Service):
    def initialize(self):
        '''
        Setup AppLogic Service
        '''
        self.sapnotes = {}
        self.stats = {}
        self.stats['maincomp'] = {}
        self.stats['cats'] = {}
        self.stats['component'] = set()
        self.stats['category'] = set()
        self.stats['priority'] = set()
        self.stats['type'] = set()
        self.stats['version'] = set()
        #~ self.stats['releaseon'] = set()
        #~ self.rebuild_from_dir()


    def store(self, sapnote, html):
        DB_DIR = self.get_var('DB', 'local')
        FSAPNOTE = DB_DIR + sapnote + '.xml'

        try:
            f = open(FSAPNOTE, 'w')
            f.write(html)
            f.close()
            self.log.debug("\tSAP Note %s stored in %s" % (sapnote, FSAPNOTE))
        except Exception as error:
            self.log.error(error)


    def rebuild_from_dir(self, path=None):
        db = self.get_service('DB')
        DB_DIR = self.get_var('DB', 'local')

        #~ FSAPNOTE = DB_DIR + sid + '.xml'
        if path is None:
            path = DB_DIR

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

        cb =self.app.get_service('Callbacks')
        cb.refresh_view()


    def get_sapnote_content(self, sid):
        DB_DIR = self.get_var('DB', 'local')
        FSAPNOTE = DB_DIR + sid + '.xml'
        content = open(FSAPNOTE, 'r').read()
        return content


    def is_stored(self, sid):
        DB_DIR = self.get_var('DB', 'local')
        fsapnote = DB_DIR + sid + '.xml'
        stored = os.path.exists(fsapnote)
        #~ self.log.debug("\tSAP Note %s stored in database? %s" % (sid, stored))

        return stored


    def build_stats(self, bag=None):
        if bag is None:
            bag = self.sapnotes
        self.dstats = {}
        self.compstats = {}
        alltasks = set()

        for sid in bag:
            # tasks
            try:
                tasks = self.sapnotes[sid]['tasks']
                for task in tasks:
                    alltasks.add(task)
            except: pass
            self.tasks = self.app.get_service('Tasks')
            self.tasks.save_tasks_from_stats(alltasks)

            # components
            compkey = self.sapnotes[sid]['componentkey']
            comptxt = self.sapnotes[sid]['componenttxt']
            #~ self.log.debug("%s -> %s -> %s" % (sid, compkey, comptxt))
            component = escape("%s (%s)" % (compkey, comptxt))
            sep = compkey.find('-')
            if sep > 0:
                maincomp = compkey[0:sep]
            else:
                maincomp = compkey

            # categories
            category = escape(self.sapnotes[sid]['category'])
            try:
                cont = self.stats['cats'][category]
                self.stats['cats'][category] = cont + 1
            except:
                self.stats['cats'][category] = 1

            # Build all (sub)keys from given component key
            # useful for display stats with pygal
            compkeys = compkey.split('-')
            total = len(compkeys)
            key = ''
            i = 0
            for subkey in compkeys:
                key = key + '-' + subkey
                if key[:1] == '-':
                    key = key[1:]

                # update stats
                try:
                    count = self.compstats[key]
                    self.compstats[key] = count + 1
                except Exception as error:
                    self.compstats[key] = 1

            try:
                cont = self.stats['maincomp'][maincomp]
                self.stats['maincomp'][maincomp] = cont + 1
            except:
                self.stats['maincomp'][maincomp] = 1

            category = escape(self.sapnotes[sid]['category'])
            priority = escape(self.sapnotes[sid]['priority'])
            ntype = escape(self.sapnotes[sid]['type'])
            version = escape(self.sapnotes[sid]['version'])
            releaseon = escape(self.sapnotes[sid]['releaseon'])
            self.stats['component'].add(component)
            self.stats['category'].add(category)
            self.stats['priority'].add(priority)
            self.stats['type'].add(ntype)
            self.stats['version'].add(version)
            #~ self.stats['releaseon'].add(releaseon)
            #~ self.stats[''].add(version)
        #~ self.log.debug(self.compstats)
        #~ self.log.debug("==")
        #~ self.log.debug(self.stats)
        #~ self.log.debug(self.stats['maincomp'])


    def get_stats(self):
        return self.stats


    def add(self, sapnote):
        sid = sapnote['id']
        self.sapnotes[sid] = sapnote


    def add_list(self, sapnotes):
        for sapnote in sapnotes:
            sid = sapnote['id']
            self.sapnotes[sid] = sapnote


    def get_notes(self):
        '''
        Return all sapnotes
        '''
        return self.sapnotes


    def get_total(self):
        '''
        Return total sapnotes
        '''
        return len(self.sapnotes)


    def load_notes(self):
        '''
        If notes.json exists, load notes
        '''
        try:
            fnotes = self.get_file('SAP')
            with open(fnotes, 'r') as fp:
                self.sapnotes = json.load(fp)
                self.log.debug ("Loaded %d notes" % len(self.sapnotes))
        except Exception as error:
            self.log.info("SAP Notes database not found. Creating a new one")
            self.save_notes()


    def get_sapnote_metadata(self, sid):
        try:
            return self.sapnotes[sid]
        except KeyError as error:
            self.log.warning("SAP Note %s doesn't exist in the database" % sid)
            return None

    #~ def save_notes(self, filename='', bag={}):
        #~ '''
        #~ Save SAP Notes to file
        #~ '''
        #~ if len(filename) == 0:
            #~ filename = self.get_file('SAP')
            #~ bag = self.sapnotes

        #~ fnotes = open(filename, 'w')
        #~ json.dump(bag, fnotes)
        #~ fnotes.close()
        #~ self.log.info ("Saved %d notes to %s" % (len(bag), filename))


    def save_notes(self, bag={}, export_path=None):
        '''
        Save SAP Notes to json database file
        '''
        if export_path is None:
            export_path = self.get_file('SAP')

        if len(bag) == 0:
            bag = self.get_notes()

        fdb = open(export_path, 'w')
        json.dump(bag, fdb)
        fdb.close()
        self.log.info ("Saved %d notes to %s" % (len(bag), export_path))


    def export(self, bag, export_path=None):
        pass


    def export_basico_package(self, bag, target):
        self.save_notes(bag, target)
        #~ TMP_DIR = LPATH['TMP']
        #~ PKG_DIR = TMP_DIR + 'basico'
        #~ BCO_SAPNOTES = PKG_DIR + SEP + 'sapnotes.json'
        #~ TARGET = export_path + SEP + '.bco'

        # 0 Delete temporary package dir
        #~ try:
            #~ shutil.rmtree(PKG_DIR)
            #~ self.log.debug("Temporary package dir deleted: '%s'" % PKG_DIR)
        #~ except: pass

        # 1 Create temporary dir for building a basico package
        #~ os.mkdir(PKG_DIR)
        #~ self.log.debug("Temporary package dir created: '%s'" % PKG_DIR)

        # 2 Export selected SAP Notes to basico package directory
        #~ self.save_notes(bag, BCO_SAPNOTES)

        # 3 Create Basico Package
        #~ utils = self.get_service('Utils')
        #~ utils.zip('basico_package', PKG_DIR)

        # 4 Delete temporary dir
        #~ shutil.rmtree(PKG_DIR)
        #~ self.log.debug("Temporary package dir deleted: '%s'" % PKG_DIR)


    def get_property_count(self, prop):
        found = 0

        store = self.get_notes()
        for sid in store:
            try:
                store[sid][prop]
                found += 1
            except:
                pass

        return found


    def get_linked_projects(self, sapnote):
        try:
            projects = self.sapnotes[sapnote]['projects']
        except Exception as error:
            projects = []

        return projects


    def get_linked_tasks(self, sapnote):
        try:
            tasks = self.sapnotes[sapnote]['tasks']
        except Exception as error:
            tasks = []
        self.log.debug("Tasks: %s" % tasks)
        return tasks


    def link_to_task(self, sapnotes, tasks):
        for sapnote in sapnotes:
            try:
                self.sapnotes[sapnote]['tasks'] = tasks
                self.log.info("Linked SAP Note %s to task(s): %s" % (sapnote, tasks) )
            except:
                self.log.error(self.get_traceback())


    def import_sapnotes(self, bag):
        for sid in bag:
            # Check if SAP Note exists in main database
            found = self.get_sapnote_metadata(sid)
            if found is None:
                self.sapnotes[sid] = bag[sid]
            else:
                # Import only tasks
                try:
                    imptasks = bag[sid]['tasks']
                    tasks = self.sapnotes[sid]['tasks']
                    tasks.extend(imptasks)
                    self.sapnotes[sid]['tasks'] = tasks
                except Exception as error:
                    self.log.error(error)
                    pass
                # Import other metadata


    def set_bookmark(self, sapnotes):
        for sapnote in sapnotes:
            self.log.info("SAP Note %s bookmarked: True" % sapnote)
            self.sapnotes[sapnote]['bookmark'] = True
        self.save_notes()


    def set_no_bookmark(self, sapnotes):
        for sapnote in sapnotes:
            self.log.info("SAP Note %s bookmarked: False" % sapnote)
            self.sapnotes[sapnote]['bookmark'] = False
        self.save_notes()


    def is_bookmark(self, sapnote):
        try:
            return self.sapnotes[sapnote]['bookmark']
        except:
            return False


    def delete(self, sapnote):
        deleted = False
        try:
            del (self.sapnotes[sapnote])
            deleted = True
        except:
            deleted = False

        return deleted


    def run(self):
        self.load_notes()
        self.build_stats()


    def end(self):
        self.save_notes()

