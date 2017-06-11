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

import pyinotify
import time
import logging
from os.path import dirname
import hcpup


class EventHandler(pyinotify.ProcessEvent):
    """
    Handle the inotify events.
    """
    global NOTIFIER

    def __init__(self, queues):
        """
        :param queue: the queues object
        """
        self.logger = logging.getLogger(__name__+'.EventHandler')
        self.queues = queues

    def process_IN_CREATE(self, event):
        """
        Event triggered in case something has been created into the
        watched folder. We're just interested in directories, as they need
        some special handling to make sure we don't loose files.

        :param event:   the event object
        """
        if event.dir:
            if not event.pathname in self.queues.doubledirs.keys():
                with self.queues.knownfileslock:
                    self.queues.knownfiles[event.pathname] = []
                    self.queues.rvqueue.put((9, event.pathname))
                self.queues.doubledirs[event.pathname] = time.time()
                self.logger.debug('CREATED: {}'.format(event.pathname))
            else:
                self.logger.debug('duplicate CREATE event for {}'
                                  .format(event.pathname))

    def process_IN_MOVED_TO(self, event):
        """
        Event triggered in case something has been moved into the
        watched folder.

        :param event:   the event object
        """
        if not event.dir:
            self._process_newfile(event)
            self.logger.debug('file MOVED_TO: {}'.format(event.pathname))
        else:
            if not event.pathname in self.queues.doubledirs.keys():
                with self.queues.knownfileslock:
                    self.queues.knownfiles[event.pathname] = []
                    self.queues.rvqueue.put((9, event.pathname))
                self.queues.doubledirs[event.pathname] = time.time()
                self.logger.debug('MOVED_TO: {}'.format(event.pathname))
            else:
                self.logger.debug('duplicate CREATE event for {}'
                                  .format(event.pathname))


    def process_IN_CLOSE_WRITE(self, event):
        """
        Event triggered in case something has been written or moved into the
        watched folder.

        :param event:   the event object
        """
        if not event.dir:
            self._process_newfile(event)
            self.logger.debug('file CLOSE_WRITE: {}'.format(event.pathname))

    def process_IN_DELETE(self, event):
        """
        Event triggered in case something has been deleted.

        :param event:   the event object
        """
        if event.dir:
            wd = self.queues.watchmgr.get_wd(event.pathname)
            self.logger.debug('watchmgr.get_wd({}) = {}'.format(event.pathname,
                                                                wd))
            self.queues.watchmgr.del_watch(wd)
            if event.dir in self.queues.doubledirs.keys():
                del self.queues.doubledirs[event.dir]
            self.logger.debug('successfully unwatched dir {}'
                              .format(event.pathname))

    def _process_newfile(self, event):
        """
        Process a new file.

        :param event:   the event object
        """
        d = dirname(event.pathname)
        with self.queues.knownfileslock:
            self.logger.debug('*** lock set (EventHandler) ***')
            if d in self.queues.knownfiles.keys():
                self.queues.knownfiles[d].append(event.pathname)
            if event.pathname in self.queues.dcdict.keys():
                self.logger.debug('double: {} already grabbed by dircrawler'
                                  .format(event.pathname))
                del self.queues.dcdict[event.pathname]
            else:
                self.queues.queue.put((9, event.pathname))
                if not hcpup.QUEUEINUSE.is_set():
                    hcpup.QUEUEINUSE.set()
            self.logger.debug('*** lock released (EventHandler) ***')

    def process_IN_Q_OVERFLOW(self, event):
        """
        Event triggered in case something has been written or moved into the
        watched folder.

        :param event:   the event object
        """
        hcpup.QUEUEOVERFLOWEVENT.set()
        self.logger.warning('inotify queue overflow - dirscan scheduled')


class Notify(object):
    def __init__(self, watchdir, queue):
        """
        Activate inotify on our watchdir.

        :param watchdir:    the directory to watch for events
        :param queue:       the queue where newly arrived files go in for upload
        :return:            nothing
        """
        self.logger = logging.getLogger(__name__+'.Notify')
        self.logger.debug('initializing inotify')
        self.watchdir = watchdir
        self.queue = queue

        pyinotify.log.setLevel(logging.ERROR)

        self.wm = pyinotify.WatchManager()  # Watch Manager

        # watched events - we keep it as tight as possible to lower the chance
        # we miss something
        self.mask = pyinotify.IN_MOVED_TO | pyinotify.IN_CLOSE_WRITE | \
                    pyinotify.IN_CREATE | pyinotify.IN_Q_OVERFLOW | \
                    pyinotify.IN_DELETE

        self.notifier = pyinotify.ThreadedNotifier(self.wm,
                                                   EventHandler(self.queue))
        self.notifier.start()

        self.wdd = self.wm.add_watch(watchdir, self.mask, rec=True,
                                     auto_add=True)
        self.logger.debug(hcpup.log.dpprint('WatchManager content:',
                                            [x.path for x in
                                             self.wm.watches.values()]))

        if self.wdd[watchdir] < 0:  # Error!
            self.stop()
            self.logger.error('Fatal: adding watch to {} failed!'
                              .format(watchdir))
            raise OSError('Fatal: adding watch to {} failed!'
                          .format(watchdir))
        else:
            self.logger.info('hcpupd is watching folder {} (and subdirs)'
                             .format(watchdir))

    def add_watch(self, watchdir):
        """
        Add another folder to the list of watched folders.
        Used in case the queue faced an overflow and a dir gets lost.
        
        :param watchdir:    the folder to add 
        """
        return self.wm.add_watch(watchdir, self.mask, rec=True, auto_add=True)

    def scheduleexisting(self):
        """
        Schedule existing  files to be uploaded.

        :returns:   the number of folders scheduled
        """
        self.logger.debug('size of queue = {}, rvqueue = {}'
                            .format(self.queue.queue.qsize(),
                                    self.queue.rvqueue.qsize()))

        self.queue.rvqueue.put((9, self.watchdir))

        # cnt = 0
        # for w in self.wdd:
        #     if self.wdd[w]:
        #         self.queue.rvqueue.put((9, w))
        #         cnt += 1

        self.logger.debug('scheduled directory scan for {}'
                          .format(self.watchdir))

    def stop(self):
        """
        Disable the notifier
        """
        self.logger.debug('disabling inotify')
        self.notifier.stop()
        del self.notifier
        time.sleep(.5)
