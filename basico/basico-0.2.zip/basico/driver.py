#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: driver.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Selenium Driver service

import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .service import Service

GECKODRIVER_URL = "https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz"

class SeleniumDriver(Service):
    def initialize(self):
        self.driver = None


    def open(self):
        '''
        In order to have selenium working with Firefox and be able to
        get SAP Notes from launchpad.support.sap.com you must:
        1. Use a browser certificate (SAP Passport) in order to avoid
           renewed logons.
           You can apply for it at:
           https://support.sap.com/support-programs-services/about/getting-started/passport.html
        2. Get certificate and import it into Firefox.
           Open menu -> Preferences -> Advanced -> View Certificates
           -> Your Certificates -> Import
        3. Trust this certificate (auto select)
        4. Check it. Visit some SAP Note url in Launchpad.
           No credentials will be asked.
           Launchpad must load target page successfully.
        '''

        if self.driver is None:
            utils = self.get_service('Utils')
            FIREFOX_PROFILE_DIR = utils.get_firefox_profile_dir()
            FIREFOX_PROFILE = webdriver.FirefoxProfile(FIREFOX_PROFILE_DIR)
            driver = webdriver.Firefox(FIREFOX_PROFILE)
            self.driver = driver
            self.log.debug("Webdriver initialited")

        return self.driver


    def close(self):
        try:
            self.driver.quit()
            self.log.debug("\tWebdriver closed")
        except:
            self.log.debug("Webdriver already closed")
            pass

        self.driver = None



    def load(self, URL):
        driver = self.open()
        driver.get(URL)
        return driver


    def check(self):
        """
        Check gecko webdriver
        You must install geckodriver. It is mandatory
        Yo can download it from:
        https://github.com/mozilla/geckodriver/
        Then, extract the binary and copy it to somewhere in your $PATH.
        If OS is Linux: /usr/local/bin/geckodriver
        If OS is Windows: C:\Windows\System32 or elsewhere.

        Basico will try to do it for you.
        """
        utils = self.get_service('Utils')

        # First, add BASICO OPT Path to $PATH
        GECKO_INSTALL_DIR = self.get_var('DRIVERS', 'local')
        os.environ["PATH"] += os.pathsep + GECKO_INSTALL_DIR
        # Then, look for Geckodriver
        GECKODRIVER = utils.which('geckodriver')

        if not GECKODRIVER:
            self.log.debug("Attempting to download and install it.")
            utils.install_geckodriver()

        GECKODRIVER = utils.which('geckodriver')
        if GECKODRIVER is None:
            self.log.warning("Gecko driver not found.")
            return False
        else:
            self.log.debug("Gecko Webdriver found in: %s" % GECKODRIVER)
            return True


    def run(self):
        pass


    def quit(self):
        self.close()


    def end(self):
        self.close()


