#!python
# -*- coding: utf-8 -*-
"""
File : pyhaystack.py (2.x)
THIS IS INCOMPLETE WORK
Would allow a shell connection to haystack server

This module allow a connection to a haystack server
Feautures provided allow user to fetch data from the server and eventually, to post to it.

See http://www.project-haystack.org for more details

Project Haystack is an open source initiative to streamline working with data from the Internet of Things. We standardize semantic data models and web services with the goal of making it easier to unlock value from the vast quantity of data being generated by the smart devices that permeate our homes, buildings, factories, and cities. Applications include automation, control, energy, HVAC, lighting, and other environmental systems.

"""


import requests
import json
import pandas as pd
import numpy as np
from pandas import Series
import matplotlib.pyplot as plt
import csv
import re,datetime
import os
import re
import sys
import getopt
#import fnmatch
import time
#import subprocess
#from subprocess import PIPE, call, Popen
#import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#import shlex

#from configobj import ConfigObj
#from os.path import expanduser
#import os
#from time import strftime

#import pyhaystack.pyhaystack.client.NiagaraAXConnect
import pyhaystack.client.NiagaraAXClient as ax

def hconnect(address,user,password):
    session = ax.Connect(address,user,password)


def usage():
    print("Usage: %s [OPTIONS]" % (sys.argv[0]))
    print("Check multiple git repository in one pass")
    print("== Common options ==")
    print("  -v, --verbose                        Show console messages")
    print("  -a <url>, --address=<url>            url address of Haystack server to connect to")
    print("  -u <username>, --user=<username>     Username")
    print("  -p <password>, --password=<password> Password")


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "vh:a:u:p",
            ["verbose", "help","address=", "user=", "password="])
    except getopt.GetoptError as e:
        if e.opt == 'a' and 'requires argument' in e.msg:
            print("Please indicate url address")
        else:
            print(e.msg)
        sys.exit(2)

    verbose = False
    #checkremote = False
    #email = False
    watchInterval = 0
    #bellOnActionNeeded = False
    #searchDir = None
    #depth = None
    #quiet = False
    #ignoreBranch = r'^$'  # empty string
    address = "http://localhost/haystack/about"
    user = None
    password = None
    for opt, arg in opts:
        if opt in ("-v", "--verbose"):
            verbose = True
        #elif opt in ("-r", "--remote"):
        #    checkremote = True
        #elif opt in ("-r", "--remote"):
        #    checkremote = True
        #elif opt in ("-b", "--bell"):
        #    bellOnActionNeeded = True
        #elif opt in ("-w", "--watch"):
        #    try:
        #        watchInterval = float(arg)
        #    except ValueError:
        # #       print "option %s requires numeric value" % opt
        #        sys.exit(2)
        elif opt in ("-a", "--address"):
            address = arg
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-p", '--password'):
            password = arg
        #    try:
        #        depth = int(arg)
        #    except ValueError:
        #        print "option %s requires int value" % opt
        #        sys.exit(2)
        #elif opt in ("-q", "--quiet"):
        #    quiet = True
        #elif opt in ("-e", "--email"):
        #    email = True
        #elif opt in ("--initEmail"):
        #    initEmailConfig()
        #    sys.exit(0)
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            print("Unhandled option %s" % opt)
            sys.exit(2)

    while True:
        hconnect(
            verbose,
            address,
            user,
            password
        )

        if watchInterval:
            time.sleep(watchInterval)
        else:
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    #Test should be in this file somewhere...


