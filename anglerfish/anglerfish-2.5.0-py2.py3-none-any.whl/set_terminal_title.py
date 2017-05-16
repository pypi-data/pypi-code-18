#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Set or Reset CLI Window Titlebar Title."""


import sys

from shutil import which
from subprocess import run


def set_terminal_title(titlez=""):
    """Set or Reset CLI Window Titlebar Title."""
    if titlez and isinstance(titlez, str) and len(titlez.strip()):
        if sys.platform.startswith('win') and which("title"):  # Windows
            run("{} {}".format(which("title"), titlez), shell=True, timeout=3)
        else:  # Linux, Os X and otherwise
            print(r"\x1B]0; {0} \x07".format(titlez.strip()))
        return titlez
    else:
        if sys.platform.startswith('win') and which("title"):
            run(str(which("title")), shell=True, timeout=3)
        else:
            print(r"\x1B]0;\x07")
        return ""  # Title should be "" so we return ""
