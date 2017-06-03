#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: env.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Environment variables

import sys
import os
from os.path import abspath, sep as SEP

ROOT = abspath(sys.modules[__name__].__file__ + "/..")
USER_DIR = os.path.expanduser('~')

# App Info
APP = {}
APP['short'] = "basico"
APP['name'] = "SAP Notes Manager for SAP Consultants"
APP['desc'] = "SAP Notes Manager for SAP Consultants\n\nThe code is licensed under the terms of the  GPL v3 so you're free to grab, extend, improve and fork the code as you want"
APP['version'] = "0.2"
APP['authors'] = ["Tomás Vírseda <t00m@t00mlabs.net>"]
APP['documenters'] = ["Tomás Vírseda <t00m@t00mlabs.net>"]
APP['email'] = "t00m@t00mlabs.net"

# Local paths
LPATH = {}
LPATH['ROOT'] = USER_DIR + SEP + '.basico' + SEP
LPATH['ETC'] = LPATH['ROOT'] + 'etc' + SEP
LPATH['VAR'] = LPATH['ROOT'] + 'var' + SEP
LPATH['PLUGINS'] = LPATH['VAR'] + 'plugins' + SEP
LPATH['LOG'] = LPATH['VAR'] + 'logs' + SEP
LPATH['TMP'] = LPATH['VAR'] + 'tmp' + SEP
LPATH['DB'] = LPATH['VAR'] + 'db' + SEP
LPATH['EXPORT'] = LPATH['VAR'] + 'export' + SEP
LPATH['OPT'] = LPATH['ROOT'] + 'opt' + SEP
LPATH['DRIVERS'] = LPATH['OPT'] + 'webdrivers' + SEP
LPATH['RES'] = LPATH['ROOT'] + 'res' + SEP

# Global paths
GPATH = {}
GPATH['ROOT'] = ROOT
GPATH['DATA'] = GPATH['ROOT'] + SEP  + 'data' + SEP
GPATH['UI'] = GPATH['DATA'] + 'ui' + SEP
GPATH['ICONS'] = GPATH['DATA'] + 'icons' + SEP
GPATH['PLUGINS'] = GPATH['DATA'] + 'plugins' + SEP
GPATH['SHARE'] = GPATH['DATA'] + 'share' + SEP
GPATH['DOC'] = GPATH['SHARE'] + 'docs' + SEP
GPATH['RES'] = GPATH['DATA'] + 'res' + SEP

# Configuration, SAP Notes Database and Log files
FILE = {}
FILE['TASKS'] = LPATH['ETC'] + 'tasks.txt'
FILE['CNF'] = LPATH['ETC'] + 'basico.ini'
FILE['SAP'] = LPATH['DB'] + 'sapnotes.json'
FILE['LOG'] = LPATH['LOG'] + 'basico.log'
FILE['CREDITS'] = GPATH['DOC'] + 'CREDITS'

# SAP related
SAP = {}
SAP['NOTE_URL'] = "https://launchpad.support.sap.com/#/notes/%s"
SAP['ODATA_NOTE_URL'] = "https://launchpad.support.sap.com/services/odata/svt/snogwscorr/TrunkSet(SapNotesNumber='%s',Version='0',Language='E')" #$expand=LongText" #?$expand=LongText,RefTo,RefBy"

