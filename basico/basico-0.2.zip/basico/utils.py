#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: utils.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Generic functions service

import os
import sys
import subprocess
import tarfile
import zipfile
import shutil
import urllib.request
import requests
import webbrowser
import feedparser

from .service import Service

class Utils(Service):
    def initialize(self):
        self.uas = []


    def browse(self, lurl):
        if sys.platform in ['linux', 'linux2']:
            browser = webbrowser.get('firefox')
        elif sys.platform == 'win32':
            browser = webbrowser.get('windows-default')

        for url in lurl:
            self.log.debug("Browsing URL: %s" % url)
            browser.open_new_tab(url)


    def which(self, program):
        if sys.platform == 'win32':
            program = program + '.exe'

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None


    def install_geckodriver(self):
        """Get last version of Gecko webdriver from github"""
        self.log.debug("OS Platform: %s" % sys.platform)
        if sys.platform in ['linux', 'linux2']:
            GECKO_SOURCE = "https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz"
            GECKO_TARGET = self.get_var('TMP', scope='local') + 'gecko.tar.gz'
        elif sys.platform == 'win32':
            GECKO_SOURCE = "https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-win64.zip"
            GECKO_TARGET = self.get_var('TMP', scope='local') + 'gecko.zip'

        GECKO_INSTALL_DIR = self.get_var('DRIVERS', 'local')


        if os.path.exists(GECKO_TARGET):
            self.log.debug("Gecko webdriver already downloaded")
            downloaded = True
        else:
            downloaded = self.download('Gecko', GECKO_SOURCE, GECKO_TARGET)

        if downloaded:
            if sys.platform in ['linux', 'linux2']:
                extracted = self.extract(GECKO_TARGET, GECKO_INSTALL_DIR, 'tar.gz')
            elif sys.platform == 'win32':
                extracted = self.extract(GECKO_TARGET, GECKO_INSTALL_DIR, 'zip')
            if extracted:
                self.log.debug("Gecko webdriver deployed successfully")
            else:
                self.log.error("Gecko could not be deployed")
                self.log.error("Tip: maybe %s is corrupt. Delete it" % GECKO_TARGET)
                #FIXME: stop application gracefully
                exit(-1)


    def download(self, prgname, source, target):
        try:
            self.log.debug ("Downloading %s from: %s" % (prgname, source))
            response = requests.get(source, stream=True)
            with open(target, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            self.log.debug ("%s downloaded to %s" % (prgname, target))
            return True
        except Exception as error:
            self.log.error(error)
            return False


    def extract(self, filename, target_path, protocol):
        self.log.debug("Extracting %s to %s using protocol %s" % (filename, target_path, protocol))
        if protocol in ['tar.gz', 'bz2']:
            try:
                tar = tarfile.open(filename, "r:*")
                tar.extractall(target_path)
                tar.close()
                self.log.debug("Extracted successfully")
                return True
            except Exception as error:
                self.log.error(error)
                return False
        elif protocol == 'zip':
            try:
                self.unzip(filename, target_path)
                self.log.debug("Extracted successfully")
                return True
            except Exception as error:
                self.log.error(error)
                return False

    def zip(self, filename, directory):
        # http://stackoverflow.com/a/25650295
        #~ make_archive(archive_name, 'gztar', root_dir)
        res = shutil.make_archive(filename, 'gztar', directory)
        self.log.debug("%s - %s" % (filename, directory))
        self.log.debug("zip res: %s" % res)


    def unzip(self, target, install_dir):
        zip_archive = zipfile.ZipFile(target, "r")
        zip_archive.extractall(path=install_dir)
        zip_archive.close()


    def get_firefox_profile_dir(self):
        if sys.platform in ['linux', 'linux2']:
            cmd = "ls -d /home/$USER/.mozilla/firefox/*.default/"
            p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
            FF_PRF_DIR = p.communicate()[0][0:-2]
            FF_PRF_DIR_DEFAULT = str(FF_PRF_DIR,'utf-8')
        elif sys.platform == 'win32':
            import glob
            APPDATA = os.getenv('APPDATA')
            FF_PRF_DIR = "%s\\Mozilla\\Firefox\\Profiles\\" % APPDATA
            PATTERN = FF_PRF_DIR + "*default*"
            FF_PRF_DIR_DEFAULT = glob.glob(PATTERN)[0]

        return FF_PRF_DIR_DEFAULT


    def feedparser_parse(self, thing):
        try:
            return feedparser.parse(thing)
        except TypeError:
            if 'drv_libxml2' in feedparser.PREFERRED_XML_PARSERS:
                feedparser.PREFERRED_XML_PARSERS.remove('drv_libxml2')
                return feedparser.parse(thing)
            else:
                self.log.error(self.get_traceback())
                return None
