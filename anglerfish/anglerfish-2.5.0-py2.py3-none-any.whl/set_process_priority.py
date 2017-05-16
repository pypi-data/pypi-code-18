#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Set process I/O and cpu priority."""


import atexit
import logging as log
import os

from shutil import which
from subprocess import Popen, call


def set_process_priority(nice=True, ionice=False, cpulimit=0):
    """Set process name and cpu priority."""
    w = " may delay I/O Operations, not recommended on user-facing GUI!."
    try:
        if nice:
            old = os.getpriority(os.PRIO_PROCESS, 0)
            os.nice(19)  # smooth cpu priority
            log.debug("Process CPUs Priority set: from {0} to 19.".format(old))
        elif ionice and which("ionice"):
            log.warning("ionice" + w)
            command = "{0} --ignore --class 3 --pid {1}".format(
                which("ionice"), os.getpid())
            call(command, shell=True)  # I/O nice,should work on Linux and Os X
            log.debug("Process I/O Priority set to: {0}.".format(command))
        elif cpulimit and which("cpulimit"):
            log.warning("cpulimit" + w)
            log.debug("Launching 1 background 'cpulimit' child subprocess...")
            cpulimit = int(cpulimit if cpulimit > 4 else 5)  # makes 5 the min.
            command = "{0} --include-children --pid={1} --limit={2}".format(
                which("cpulimit"), os.getpid(), cpulimit)
            proces = Popen(command, shell=True)  # This launch a subprocess.
            atexit.register(proces.kill)  # Force Kill subprocess at exit.
            log.debug("Process CPUs Max Limits capped to: {0}".format(command))
    except Exception as error:
        log.warning(error)
        return False  # this may fail on windows and its normal, so be silent.
    else:
        return True
