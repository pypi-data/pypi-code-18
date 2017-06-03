#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: settings.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Settings service


from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Pango
from gi.repository.GdkPixbuf import Pixbuf

from .service import Service

# Default settings for SAP module
LOGIN_PAGE_URL = "https://accounts.sap.com"
LOGOUT_PAGE_URL = "https://accounts.sap.com/ui/logout"
ODATA_NOTE_URL = "https://launchpad.support.sap.com/services/odata/svt/snogwscorr/TrunkSet(SapNotesNumber='%s',Version='0',Language='E')" #$expand=LongText" #?$expand=LongText,RefTo,RefBy"
SAP_NOTE_URL = "https://launchpad.support.sap.com/#/notes/%s"
SAP_NOTE_URL_PDF = "https://launchpad.support.sap.com/services/pdf/notes/%s/E"
TIMEOUT = 5


class Settings(Service):
    def initialize(self):
        view = self.get_config_value('View')
        self.log.debug("View: %s" % view)

    def get_default_settings(self):
        settings = {}
        # Deprecated as Basico uses now login with SAP Passport
        #~ settings['CNF_SAP_SUser'] = 'SXXXXXXXXXX'
        #~ settings['CNF_SAP_SPass'] = 'MyP455w0rD'
        utils = self.get_service('Utils')
        settings['CNF_SAP_LOGIN'] = LOGIN_PAGE_URL
        settings['CNF_SAP_LOGOUT'] = LOGOUT_PAGE_URL
        settings['CNF_SAP_ODATA_NOTES'] = ODATA_NOTE_URL
        settings['CNF_SAP_NOTE_URL'] = SAP_NOTE_URL
        settings['CNF_SAP_CONN_TIMEOUT'] = TIMEOUT
        settings['CNF_FF_PROFILE_DIR'] = utils.get_firefox_profile_dir()

        return settings


    def get_custom_settings(self):
        sap = self.get_service('SAP')
        utils = self.get_service('Utils')

        settings = {}
        settings['CNF_SAP_LOGIN'] = sap.get_config_value('CNF_SAP_LOGIN')
        settings['CNF_SAP_LOGOUT'] = sap.get_config_value('CNF_SAP_LOGOUT')
        settings['CNF_SAP_ODATA_NOTES'] = sap.get_config_value('CNF_SAP_ODATA_NOTES')
        settings['CNF_SAP_NOTE_URL'] = sap.get_config_value('CNF_SAP_NOTE_URL')
        settings['CNF_SAP_CONN_TIMEOUT'] = sap.get_config_value('CNF_SAP_CONN_TIMEOUT')
        settings['CNF_FF_PROFILE_DIR'] = sap.get_config_value('CNF_FF_PROFILE_DIR')

        return settings
