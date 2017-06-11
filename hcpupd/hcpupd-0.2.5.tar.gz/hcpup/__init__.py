# The MIT License (MIT)
#
# Copyright (c) 2017 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import argparse
from threading import Event

import hcpup.init
import hcpup.conf
import hcpup.log
# this makes sure I can run Sphinx within the project on a Mac
if sys.platform != 'darwin':
    import hcpup.notify
else:
    print('running on darwin...')
import hcpup.up
import hcpup.queue
import hcpup.service
from version import Gvars

# this will hold the hcpup.notify.Notify object, which needs to be accessible
# to allow for inotify shutdown as well as to schedule a directory scan.
NOTIFIER = None

# this event will be set by notify.EventHandler in case a queue overflow event
# has been received; the service.Timer() thread will weak up from time to time
# to see if the event has been set, and if so, trigger a dirscan to collect
# potentially lost files
QUEUEOVERFLOWEVENT = Event()

# this event will be set as soon as an entry gets into the queue; it will be
# reset if service.Timer() finds the queue empty. It is used to schedule a
# directory rescan after working the queue down to zero
QUEUEINUSE = Event()

# this will hold a threading.Event object that allows us to shutdown cleanly
# when receiving SIGINT or SIGTERM.
SHUTDOWNEVENT = Event()


def parseargs():
    """
    args - build the argument parser, parse the command line.
    """

    mainparser = argparse.ArgumentParser()
    mainparser.add_argument('--version', action='version',
                            version="%(prog)s: {0}\n"
                            .format(Gvars.Version))
    mainparser.add_argument('-c', dest='configfile',
                            default=hcpup.init.CONFIGFILE,
                            help='configuration file to be used '
                                 '(defaults to {})'
                            .format(hcpup.init.CONFIGFILE))
    mainparser.add_argument('-d', dest='daemon', action='store_true',
                            default=False,
                            help='enable *nix daemon mode')

    result = mainparser.parse_args()
    return result

