import logging
import time
from os import listdir
from os.path import join, isdir
from threading import Thread

import hcpsdk
import hcpup
from hcpup.up import Uploader


class DirCrawler(Thread):
    """
    Directory Crawler - used to find files in dirs not processed by inotify.
    """
    def __init__(self, queues, *args, **kwargs):
        """
        :param queues:      the queues object (queues.queue hold the files to
                            upload)
        """
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__+'.DirCrawler')
        self.queues = queues

    def run(self):
        """
        Run the uploader thread.
        """
        self.logger.debug('{} started'.format(self.name))

        try:
            while True:
                # A single pass will always crawl a single folder, only.
                # Subfolders found in that folder will be queues for another
                # pass here.
                prio, dir = self.queues.rvqueue.get()

                # TODO: switch to debug after testing

                self.logger.info('{} got "{}" from rvqueue'
                                  .format(self.name, dir))
                self.queues.rvqueue.task_done()

                if dir == '!**exit**!':
                    self.logger.debug('{} exiting'.format(self.name))
                    break

                # get a list of all entries in dir
                try:
                    files = listdir(dir)
                except Exception as e:
                    self.logger.warning('unable to list folder {} ({}) - '
                                        're-queued'
                                        .format(dir, e))
                    self.queues.rvqueue.put((9, dir))
                    continue
                else:
                    self.logger.debug(hcpup.log.dpprint('files:', files))

                # find the files in dir that haven't been tracked by inotify
                if files:
                    with self.queues.knownfileslock:
                        self.logger.debug('*** lock set ({}) ***'
                                          .format(self.name))
                        self.logger.debug(hcpup.log.dpprint(
                            'files in {} already noticed by inotify:\n\t'
                                .format(dir),
                            [x.path for x in self.queues.watchmgr.watches.values()]))
                            # self.queues.knownfiles[
                            #     dir] if dir in self.queues.knownfiles.keys() else []))

                        left = None
                        leftfiles = []
                        leftdirs = []

                        if dir in [x.path for x in self.queues.watchmgr.watches.values()]:
                            self.logger.debug('dir = {}'.format(dir))
                            # left = [join(dir, x) for x in files if
                            #         join(dir, x) not in self.queues.knownfiles.keys()]
                            left = [join(dir, x) for x in files]
                            if dir in self.queues.knownfiles.keys():
                                del self.queues.knownfiles[dir]
                        else:
                            left = [join(dir,x) for x in files]
                        self.logger.debug(hcpup.log.dpprint('left:', left))

                        # here we sort out subdirs and files; dirs are checked
                        # for being watches, added to watches if they aren't
                        # and scheduled for a dirscan as well
                        for fd in left:
                            if isdir(fd):
                                if fd in [x.path for x in self.queues.watchmgr.watches.values()]:
                                    self.queues.knownfiles[fd] = []
                                    self.queues.rvqueue.put((9, fd))
                                    self.queues.doubledirs[fd] = time.time()
                                    self.logger.debug('added {} to rvqueue'
                                                      .format(fd))
                                else:
                                    try:
                                        nw = hcpup.NOTIFIER.add_watch(fd)
                                    except Exception as e:
                                        self.logger.warning(
                                            'adding {} as watch failed '
                                            '- {}'
                                                .format(fd, e))
                                    else:
                                        self.logger.info('added {} as watch'
                                                         .format(fd))
                                        self.queues.rvqueue.put((9, fd))
                                        self.logger.debug('added {} to rvqueue'
                                                          .format(fd))
                            else:
                                leftfiles.append(fd)

                        self.logger.warning('dirscan of "{}": {} new files, '
                                            '{} new dirs'
                                            .format(dir, len(leftfiles),
                                                    len(leftdirs)))
                        self.logger.debug(hcpup.log.dpprint(
                            'files in {} not noticed by inotify:'
                                .format(dir), leftfiles))

                        for f in leftfiles:
                            self.logger.debug('putting into queue: {}'
                                              .format(f))
                            self.queues.queue.put((9, f))
                            self.queues.dcdict[f] = time.time()
                        self.logger.debug(
                            '*** lock released ({}) ***'.format(self.name))
                self.logger.debug('...end of dircrawler loop...')
        except Exception as e:
            self.logger.exception('DirCrawler failed!!!')


class Timer(Thread):
    """
    Timer - used to trigger directory re-scans.
    """
    def __init__(self, queues, *args, **kwargs):
        """
        :param queues:      the queues object (queues.queue hold the files to
                            upload)
        """
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__+'.Timer')
        self.queues = queues

    def run(self):
        """
        Monitor the QUEOVERFLOWEVENT and start a dirscan, if required.
        """
        self.logger.debug('{} started'.format(self.name))

        while True:
            # if the SHUTDOWNEVENT has been set, quit the thread
            if hcpup.SHUTDOWNEVENT.wait(60):
                break
            else:
                self.logger.info('service.Timer() triggered | '
                                 'queue.qsize() = {}, '
                                 'hcpup.QUEUEINUSE.is_set() = {}'
                                 .format(self.queues.queue.qsize(),
                                         hcpup.QUEUEINUSE.is_set()))

            # TODO: change to DEBUG after testing!

            if hcpup.QUEUEOVERFLOWEVENT.is_set():
                if self.queues.rvqueue.empty():
                    hcpup.QUEUEOVERFLOWEVENT.clear()
                    hcpup.NOTIFIER.scheduleexisting()
                    self.logger.info('QUEUEOVERFLOW triggered dirscan')
                else:
                    self.logger.info('QUEUEOVERFLOW, but rvqueue.qsize() = {},'
                                     ' no dirscan triggered'
                                     .format(self.queues.rvqueue.qsize()))
            elif self.queues.queue.empty() and hcpup.QUEUEINUSE.is_set():
                hcpup.QUEUEINUSE.clear()
                self.logger.info('drained queue triggered dirscan')
                hcpup.NOTIFIER.scheduleexisting()

        self.logger.debug('{} exiting'.format(self.name))


def startthreads(conf, target):
    """
    Start the background threads.

    :param conf:    the config object
    :param target:  the hcpsdk.Target object to use to talk to HCP
    """
    logger = logging.getLogger(__name__+'.startthreads')
    logger.debug('starting {} uploader thread(s)'
                 .format(conf['upload threads']))

    # queues (and cleanup thread)
    uwts = [hcpup.queue.Queues(name='queues')]

    # uploader threads
    uwts += [Uploader(conf, target, uwts[0], name='uploader-{:02d}'.format(i))
             for i in range(conf['upload threads'])]

    # dir crawler thread(s)
    uwts.append(hcpup.service.DirCrawler(uwts[0], name='dircrawler'))

    # timer thread
    uwts.append(hcpup.service.Timer(uwts[0], name='timer'))

    for t in uwts:
        t.setDaemon(True)
        t.start()

    return uwts


def createtarget(conf):
    """
    Create a hcpsdk.Target object used by the uploader threads.

    :param conf:    the dict from the config file
    :return:        the hcpsdk.Target object
    """
    logger = logging.getLogger(__name__+'.createtarget')
    logger.debug('setting up hcpsdk.Target({}, auth, port={})'
                 .format(conf['namespace'], 443 if conf['ssl'] else 80))

    return hcpsdk.Target(conf['namespace'],
                         hcpsdk.NativeAuthorization(conf['user'],
                                                    conf['password']),
                         port=443 if conf['ssl'] else 80,
                         dnscache=conf['local DNS resolver'])
