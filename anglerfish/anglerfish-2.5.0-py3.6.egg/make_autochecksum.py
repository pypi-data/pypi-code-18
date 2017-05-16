#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Make a automagic-checksuming file using Adler32 Hash and Hexadecimal.

Resulting on a short ~8 character checksum added to the filename,
easy to parse with standard pattern,not crypto secure but useful for checksum,
is more human friendly than SHA512 checksum and its builtin on the filename,
Adler32 is standard on all ZIP files and its builtin on Python std lib.
I do this tired of people not using SHA512 on 1 separate txt file for checksum,
this not require user command line skills to check the checksum, its automagic.
"""


import os
import pathlib

from zlib import adler32


# _REGEX = re.compile(r"(.✔\+)([\da-f])", re.I)  # (.✔+)(6 Hex char)8 total
_STANDARD_PATTERN = ".✔+"  # (check sum) use this to signal a selfchecksum


def get_autochecksum(filepath):
    with open(os.path.abspath(filepath), "rb") as fyle:
        return _STANDARD_PATTERN + hex(adler32(fyle.read()) & 0xffffffff)[2:]


def autochecksum(filepath, update=False):
    ext = "".join([_ for _ in pathlib.Path(filepath).suffixes
                   if _STANDARD_PATTERN not in _])
    filepath = os.path.abspath(filepath)
    checksum = get_autochecksum(filepath)  # Get a selfchecksum string.
    if _STANDARD_PATTERN in filepath and os.path.isfile(filepath):
        if checksum in filepath:
            return True  # File SelfChecksum is Ok, Integrity is Ok.
        elif checksum not in filepath and not update:
            return False  # File SelfChecksum is Wrong, Integrity is NOT Ok.
        elif checksum not in filepath and update:
            new_file = filepath.split(_STANDARD_PATTERN)[0] + checksum + ext
            os.rename(filepath, new_file)
            return new_file  # File SelfChecksum is Wrong, Update selfchecksum.
    elif os.path.isfile(filepath):  # File has no selfchecksum,get selfchecksum
        new_file = filepath.replace(ext, "") + checksum + ext
        os.rename(filepath, new_file)
        return new_file
