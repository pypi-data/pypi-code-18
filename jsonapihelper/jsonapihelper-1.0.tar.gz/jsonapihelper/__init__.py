"""
JSON API Helper
"""

import requests

__version__ = "1.0"
__copyright__ = "Copyright 2017-Present Kippage"
__title__ = "jsonapihelper"
__license__ = "MIT"
__author__ = "Kippage"


def check_method(string):
    global method
    if "http://" in string and string[0]=='h': method="HTTP"; return True
    elif "https://" in string and string[0]=='h': method="HTTPS"; return True
    elif "ftp://" in string and string[0]=='f': method='FTP'; return True
    else:
        return False

def get(url):
    if check_method(url):
        return requests.get(url).json()
    else:
        raise Exception('Bad method')


def post(url,data):
    if check_method(url):
        return requests.post(url,data).json()
    else:
        raise Exception('Bad method')


class Adv:
    def __init__(self):
        pass
        
    def get(self,url,params):
        if check_method(url):
            return requests.get(url,params=params).json()
        else:
            raise Exception('Bad method')

			
    def post(self,url,data,json):
        if check_method(url):
            return requests.post(url,data,json=json).json()
        else:
            raise Exception('Bad method')