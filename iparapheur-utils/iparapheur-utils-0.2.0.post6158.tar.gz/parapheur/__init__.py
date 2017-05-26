#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from requests.packages.urllib3.exceptions import SubjectAltNameWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)

"""
    Ce module est un test de client parapheur
"""
__version__ = "0.2.0-6158"


def getrestclient():
    # We have to define it here, because we use it everywhere in scripts
    import parapheur
    return parapheur.getrestclient()


def getsoapclient(user=None, password=None):
    import parapheur
    return parapheur.getsoapclient(user, password)