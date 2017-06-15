#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FIXME: this module doesn't belong in dk ).


"""Module for finding all apps folders.
"""

import os
from dk.utils import root as dkroot


def is_appfolder(path):
    """Is the ``path`` an app folder?
    """
    if os.path.isdir(path):
        if os.path.exists(os.path.join(path, 'urls.py')):
            return True
        
        if os.path.exists(os.path.join(path, 'models.py')):
            return True

        if os.path.exists(os.path.join(path, 'models')):
            return True

    return False
    

def appfolders():
    """Find all django app folders, yield absolute paths to the folders.
    """
    for dirname in os.listdir(dkroot()):
        if dirname in ('.svn', 'settings'):
            continue

        folder_path = os.path.join(dkroot(), dirname)
        if is_appfolder(folder_path):
            yield folder_path


def appfolder(appname):
    """Return app folder for ``appname``.
    """
    folder_path = os.path.join(dkroot(), appname)
    if is_appfolder(folder_path):
        return folder_path

    raise ValueError("No such app: %r." % appname)


def appname(folder):
    """Return the app name for the (app)folder).
    """
    _, app = os.path.split(folder)
    return app


def appnames():
    """Find the name of all the apps.
    """
    for folder in appfolders():
        _, app = os.path.split(folder)
        yield app


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: %s appfolders | appnames" % __file__
        sys.exit(1)

    for item in globals()[sys.argv[1]]():
        print item
