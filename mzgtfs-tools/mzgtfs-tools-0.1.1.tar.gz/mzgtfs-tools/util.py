#!/usr/bin/python
"""Utilities for mzgtfs-tools
"""

import os

def delete_temp_files(files):
    for f in files:
        if os.path.exists(f):
            os.remove(f)