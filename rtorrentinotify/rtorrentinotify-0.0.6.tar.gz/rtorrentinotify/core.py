"""core.py"""
import asyncore
import fnmatch
import logging
import os
import shutil
import subprocess
import sys

from helputils.core import log
import pyinotify

log = logging.getLogger("rtorrentinotify")
conf_path = "/etc/rtorrentinotify.conf"
conf = {}
try:
    with open(conf_path) as f:
        code = compile(f.read(), conf_path, 'exec')
        exec(code, conf)
except Exception as err:
    log.error("(E) Missing {0}. {1}".format(conf_path, err))
    sys.exit(0)
wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO


def suffix_filter(fn):

    suffixes = ["*.torrent"]
    for suffix in suffixes:
        if fnmatch.fnmatch(fn, suffix):
            return True
    return False


class EventHandler(pyinotify.ProcessEvent):
    """No need self.process_IN_CREATE(self, event), just IN_MOVE_TO"""

    def __call__(self, event):
        if suffix_filter(event.name):
            super(EventHandler, self).__call__(event)


    def process_IN_MOVED_TO(self, event):
        log.info("New torrent MOVED to gate_dir: %s" % event.pathname)
        try:
            shutil.move(event.pathname, conf["rtorrent_watchdir"])
        except:
            log.warning("Torrent exists already. Deleting torrent from gate dir.")
            os.remove(event.pathname)


def clidoor():
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(conf["gate_dir"], mask, rec=True)
    notifier.loop()
