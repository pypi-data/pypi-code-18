# Copyright (c) 2017 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""get the environmental variables
will get the heroku env vars or the local env files"""
# Extract the Environmental variables as a defaultdict
from collections import defaultdict
import os

def getenvvars(fhandle=None, defvalue=None, remoteKV=None):
    """get the environmental variables
    will get the heroku env vars or the local env files"""
    if remoteKV == None:
        remoteKV = ("ENV_NOW", "production")
    # -
    osdct = os.environ
    try:
        if osdct[remoteKV[0]] == remoteKV[1]:
            keyval = [(key, value) for key, value in osdct.items()]
    except KeyError:
        if not fhandle:
            fhandle = open(".env", 'r')
        keyval = [line.split("=") for line in fhandle.readlines()]
        keyval = [(key.strip(), value.strip()) for key, value in keyval]
    # - 
    # from https://www.accelebrate.com/blog/using-defaultdict-python/
    dct = defaultdict(lambda: defvalue)
    for key, value in keyval:
        dct[key] = value
    return dct
        
def dictvalue(dct, key, defvalue=None):
    """return the value of the dct given the key.
    return default value if key does not exist"""
    return dct.setdefault(key, defvalue)
    
    