#!python
# -*- coding: utf-8 -*-
"""
File : pyhaystackTest.py (2.x)
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
import argparse
#import fnmatch
import time
import cProfile,cStringIO,pstats
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
import pyhaystack.client.SkysparkClient as sky

def hconnect(address,user,password,proj):
    session = sky.Connect(address,user,password,proj,Zinc=False)
    return session
    pass


def main():
    pr = cProfile.Profile()
    pr.enable()
    parser = argparse.ArgumentParser(description='A pyhastack client',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--address', default="http://localhost/haystack/about",
                    help="This is the adress of the server")
    parser.add_argument('-u', '--user', default=None,
                    help="username")
    parser.add_argument('-p', '--password', default=None,
                    help="password")
    parser.add_argument('-d', '--project', default=None,
                    help="Name of the project")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="verbose output")
    args = parser.parse_args()
    verbose = False
    #checkremote = False
    #email = False
    watchInterval = 0
    #bellOnActionNeeded = False
    #searchDir = None
    #depth = None
    #quiet = False
    #ignoreBranch = r'^$'  # empty string
    address = args.address
    user = args.user
    password = args.password
    proj = args.project

    while True:
        hconnect(
            address,
            user,
            password,
            proj,
        )

        if watchInterval:
            time.sleep(watchInterval)
        else:
            break
    pr.disable()
    s = cStringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    #print s.getvalue()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    #Test should be in this file somewhere...


