#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: sap.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: SAP service

import time
import traceback
from shutil import which

from .service import Service

#~ ODATA_NOTE_URL = "https://launchpad.support.sap.com/services/odata/svt/snogwscorr/TrunkSet(SapNotesNumber='%s',Version='0',Language='E')" #$expand=LongText" #?$expand=LongText,RefTo,RefBy"
ODATA_NOTE_URL = "https://launchpad.support.sap.com/services/odata/svt/snogwscorr/TrunkSet(SapNotesNumber='%s',Version='0',Language='en')"
#~ ODATA_NOTE_URL = "https://launchpad.support.sap.com/services/odata/svt/snogwscorr/TrunkSet(SapNotesNumber='%s',Version='0',Language='E')?$expand=LongText,Languages,RefTo,RefBy"
#~ ODATA_NOTE_URL = "https://launchpad.support.sap.com/services/odata/svt/snogwscorr/TrunkSet(SapNotesNumber='%s',Version='0',Language='E')?$expand=LongText,Languages,RefTo,RefBy"
SAP_NOTE_URL = "https://launchpad.support.sap.com/#/notes/%s"
SAP_NOTE_URL_PDF = "https://launchpad.support.sap.com/services/pdf/notes/%s/E"


class SAP(Service):
    def initialize(self):
        '''
        Setup AppLogic Service
        '''
        self.__init_config_section()


    def __init_config_section(self):
        prefs = self.get_service('Settings')
        self.config = self.app.get_config()
        if self.config.has_section(self.section):
            options = self.config.options(self.section)
            if len(options) == 0:
                self.log.debug("Section %s empty. Initializing with default values" % self.section)
                settings = prefs.get_default_settings()
                self.config[self.section] = settings
                self.log.debug("Default parameters loaded:")
                for key in settings:
                    self.log.debug("\tKey: %s - Value: %s" % (key, settings[key]))
                self.save_config()


    def analyze_sapnote_metadata(self, sid, content):
        '''
        Get metadata details from SAP Note
        '''
        #~ self.log.debug("\t%s" % content)
        try:
            utils = self.get_service('Utils')
            f = utils.feedparser_parse(content)
            sid = f.entries[0].d_sapnotesnumber
            sapnote = {}
            sapnote['id'] = sid
            sapnote['componentkey'] = f.entries[0].d_componentkey
            comptxt = f.entries[0].d_componenttext
            if comptxt == "Please use note 1433157 for finding the right component":
                comptxt = ""
            sapnote['componenttxt'] = comptxt
            sapnote['category'] = f.entries[0].d_category_detail['value']
            sapnote['language'] = f.entries[0].d_languagetext_detail['value']
            sapnote['title'] = f.entries[0].d_title_detail['value']
            sapnote['priority'] = f.entries[0].d_priority_detail['value']
            sapnote['releaseon'] = f.entries[0].d_releasedon
            sapnote['type'] = f.entries[0].d_type_detail['value']
            sapnote['version'] = f.entries[0].d_version_detail['value']
            sapnote['feedupdate'] = f.entries[0].updated
            sapnote['bookmark'] = False
            self.log.info ("\tSAP Note %s analyzed successfully" % sid)
        except Exception as error:
            sapnote = {}
            self.log.error("\tError while analyzing data for SAP Note %s" % sid)
            #~ self.log.error("\t%s" % error)

        return sapnote


    def fetch(self, sid):
        db = self.get_service('DB')
        valid = False
        #~ self.log.debug("%3d/%3d - Fetching SAP Note %s" % (self.notes_fetched+1, self.notes_total, sid))

        if not db.is_stored(sid):
            self.log.debug("%3d/%3d - SAP Note %s must be downloaded" % (self.notes_fetched+1, self.notes_total, sid))
            content = self.download(sid)
            if len(content) > 0:
                self.log.debug("%3d/%3d - SAP Note %s fetched" % (self.notes_fetched+1, self.notes_total, sid))
            else:
                self.log.debug("%3d/%3d - SAP Note %s not feched" % (self.notes_fetched+1, self.notes_total, sid))
        else:
            self.log.debug("%3d/%3d - SAP Note %s will be analyzed again" % (self.notes_fetched+1, self.notes_total, sid))
            content = db.get_sapnote_content(sid)

        self.fetched()

        sapnote = self.analyze_sapnote_metadata(sid, content)
        if len(sapnote) > 0:
            db = self.get_service('DB')
            db.add(sapnote)
            db.store(sid, content)
            valid = True

        return valid, sid


    def start_fetching(self, total):
        self.notes_fetched = 0
        self.notes_total = total


    def fetched(self):
        self.notes_fetched += 1


    def stop_fetching(self):
        self.notes_fetched = 0
        self.notes_total = 0


    def download(self, sapnote=None):
        try:
            driver = self.get_service('Driver')
            #~ browser = driver.open()
            #~ self.log.debug("\tDownloading SAP Note %s:" % sapnote)
            #~ self.log.debug(ODATA_NOTE_URL % sapnote)
            browser = driver.load(ODATA_NOTE_URL % sapnote)
            time.sleep(5)
            content = browser.page_source
            #~ self.log.debug("\t%3d - SAP Note %s downloaded" % (sapnote, driver.)
            #~ else:
            #~ content = ''
        except Exception as error:
            #~ self.log.error("\tSAP Note %s coud not be downloaded" % sapnote)
            self.log.error(error)
            content = ''

        return content


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
        if len(sapnotes) == 0:
            self.log.debug("No SAP Notes selected. No task will be linked.")
            return

        db = self.get_service('DB')
        store = db.get_notes()

        for tid in sapnotes:
            sid = "0"*(10 - len(tid)) + tid
            store[sid]['tasks'] = tasks
            self.log.info("Linked SAP Note %s to task(s): %s" % (sid, tasks) )


    def set_bookmark(self, bag):
        db = self.get_service('DB')
        sapnotes = db.get_notes()
        mylist = []
        for tid in bag:
            sid = "0"*(10 - len(tid)) + tid
            sapnotes[sid]['bookmark'] = True
            mylist.append(sapnotes[sid])
            self.log.info("SAP Note %s bookmarked" % sid)
        db.add_list(mylist)


    def set_no_bookmark(self, bag):
        db = self.get_service('DB')
        sapnotes = db.get_notes()
        mylist = []
        for tid in bag:
            sid = "0"*(10 - len(tid)) + tid
            sapnotes[sid]['bookmark'] = False
            mylist.append(sapnotes[sid])
            self.log.info("SAP Note %s unbookmarked" % sid)
        db.add_list(mylist)


    def is_bookmark(self, sapnote):
        try:
            return self.sapnotes[sapnote]['bookmark']
        except:
            return False


    def run(self):
        db = self.get_service('DB')
        db.load_notes()
        db.build_stats()
