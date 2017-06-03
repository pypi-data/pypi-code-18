#!/usr/bin/python3
# -*- coding: utf-8 -*-
# File: basico.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Main entry point por Basico app
import os
# -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')
import traceback as tb
import imp
import signal
from pprint import pprint
from os.path import abspath, sep as SEP
from configparser import SafeConfigParser, ExtendedInterpolation
# import urllib.request

import selenium

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .utils import Utils
from .log import get_logger
from .gui import GUI
from .iconmanager import IconManager
from .sap import SAP
from .settings import Settings
from .uifuncs import UIFuncs
from .menus import Menus
from .projects import Projects
from .tasks import Tasks
from .plugins import Plugins
from .callbacks import Callback
from .notify import Notification
#from .stats import Stats
from .database import Database
from .driver import SeleniumDriver
from .env import ROOT, APP, LPATH, GPATH, FILE


class Basico:
    def __init__(self):
        """Main class: the entry point for Basico.
        It stands for Controller.
        """

        # Create local paths if they do not exist
        for entry in LPATH:
            if not os.path.exists(LPATH[entry]):
                os.makedirs(LPATH[entry])


        self.log = get_logger(self.__class__.__name__, FILE['LOG'])
        #~ self.log.info("Starting Basico")

        self.services = {}
        try:
            services = {
                'GUI'       :   GUI(),
                'Utils'     :   Utils(),
                'UIF'       :   UIFuncs(),
                'Menus'     :   Menus(),
                'SAP'       :   SAP(),
                'Settings'  :   Settings(),
                'Notify'    :   Notification(),
                'Tasks'     :   Tasks(),
                'IM'        :   IconManager(),
                'Plugins'   :   Plugins(),
                'Callbacks' :   Callback(),
                #'Stats'     :   Stats(),
                'DB'        :   Database(),
                'Driver'    :   SeleniumDriver()
            }
            self.register_services(services)
        except Exception as error:
            self.log.error(error)
            raise


    def setup(self):
        """
        Setup Basico Envrionment
        Info about ConfigParser options:
        https://docs.python.org/3/library/configparser.html#interpolation-of-values
        https://docs.python.org/3/library/configparser.html#configparser.ConfigParser.optionxform
        """
        self.log.debug("Setting up Basico environment")
        self.log.debug("Global path: %s" % GPATH['ROOT'])
        self.log.debug("Local path: %s" % LPATH['ROOT'])

        # Set up config
        CONFIG_FILE = self.get_file('CNF')
        self.config = SafeConfigParser(interpolation=ExtendedInterpolation())
        self.config.optionxform = str

        # Save config
        if not os.path.exists(CONFIG_FILE):
            self.log.debug('Configuration file not found. Creating a new one')
            with open(CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)
            self.log.info('Config file initialited')


    def get_config(self):
        CONFIG_FILE = self.get_file('CNF')
        self.config.read(CONFIG_FILE)

        return self.config


    def get_file(self, name):
        try:
            return FILE[name]
        except:
            self.log.error(self.get_traceback())


    def get_app_info(self, var):
        try:
            return APP[var]
        except:
            return None


    def get_var(self, name, scope='global'):
        if scope == 'global':
            return GPATH[name]
        else:
            return LPATH[name]


    def list_services(self):
        """Return a dictionary of services"""
        return self.services


    def get_service(self, name):
        """Get/Start a registered service
        @type name: name of the service
        @param name: given a service name it returns the associated
        class. If service was not running it is started.
        """
        try:
            service = self.services[name]
            if service.is_started():
                return service
            else:
                service.start(self, name)
                return service
        except KeyError as service:
            self.log.error("Service %s not registered or not found" % service)
            raise


    def register_services(self, services):
        """Register a list of services
        @type services: dict
        @param services: a dictionary of name:class for each service
        """
        for name in services:
            self.register_service(name, services[name])


    def register_service(self, name, service):
        """Register a new service
        @type name: string
        @param name: name of the service
        @type service: class
        @param service: class which contains the code
        """
        try:
            self.services[name] = service
        except Exception as error:
            self.log.error(error)


    def deregister_service(self, name):
        """Deregister a running service
        @type name: string
        @param name: name of the service
        """
        self.services[name].end()
        self.services[name] = None
        self.log.debug("Service %s stopped" % name)


    def check(self):
        '''
        Check Basico environment
        '''
        utils = self.get_service("Utils")
        uif = self.get_service('UIF')
        driver = self.get_service('Driver')

        # Show Selenium version
        self.log.debug("Selenium version: %s" % selenium.__version__)

        # Check proper GTK version
        GTK_VERSION = uif.check_gtk_version()

        # Check Gecko webdrver
        GECKO_DRIVER = driver.check()

        run = GTK_VERSION and GECKO_DRIVER

        if run:
            self.log.info("Basico environment ready!")
            return True
        else:
            self.log.error("Error(s) found checking Basico environment")
            return False




    def stop(self):
        """For each service registered, it executes the 'end' method
        (if any) to finalize them properly.
        """

        # Deregister all services loaded
        self.deregister_service('GUI')
        for name in self.services:
            try:
                if name != 'GUI':
                    self.deregister_service(name)
            except Exception as error:
                self.log.error(self.get_traceback())
                raise

        self.log.info("Basico finished")


    def get_traceback(self):
        return tb.format_exc()


    def run(self):
        try:
            self.gui = self.get_service('GUI')
            self.gui.run()
        except:
            self.log.error(self.get_traceback())


def main():
    #DOC: http://stackoverflow.com/questions/16410852/keyboard-interrupt-with-with-python-gtk
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    basico = Basico()
    basico.setup()
    ok = basico.check()
    if ok:
        basico.run()
    sys.exit(0)
