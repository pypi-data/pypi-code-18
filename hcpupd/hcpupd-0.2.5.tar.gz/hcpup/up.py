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

import logging
import time
import xml.etree.ElementTree as ET
from io import BytesIO
from os import stat, unlink, rmdir
from os.path import join, dirname, isdir
from threading import Thread

import hcpsdk
import hcpup


class Uploader(Thread):
    """
    File uploading thread.
    """
    def __init__(self, conf, target, queues, *args, **kwargs):
        """
        :param conf:        the config object
        :param target:      the hcpsdk.Target object to use to talk to HCP
        :param queues:      the queues object (queues.queue hold the files to
                            upload)
        """
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__+'.Uploader')
        self.conf = conf
        self.target = target
        self.queues = queues

    def run(self):
        """
        Run the uploader thread.
        """
        self.logger.debug('{} started'.format(self.name))

        try:
            if self.conf['obfuscate']:
                pb = hcpsdk.pathbuilder.PathBuilder(
                    initialpath=join('/rest', self.conf['path']),
                    annotation=True)

            con = hcpsdk.Connection(self.target, retries=3)

            while True:
                prio, item = self.queues.queue.get()
                self.logger.debug('{} got "{}" from queue'.format(self.name,
                                                                  item))
                self.queues.queue.task_done()

                if item == '!**exit**!':
                    self.logger.debug('{} exiting'.format(self.name))
                    break

                # skip directories
                if isdir(item):
                    self.logger.debug('{} is a directory - skipping'
                                      .format(item))
                    continue

                try:
                    with open(item, 'rb') as itemhdl:
                        if self.conf['obfuscate']:
                            px = pb.getunique(item)
                            url = join(px[0], px[1])
                            annotation = self.fixannotation(item, px[2])
                        else:
                            url = join('/rest', self.conf['path'],
                                       item[len(self.conf['watchdir']) + 1:])

                        try:
                            con.PUT(url, body=itemhdl)
                        except hcpsdk.HcpsdkError as e:
                            self.logger.warning(hcpup.log.dpprint(
                                'PUT {} ({}) failed - hint:'
                                    .format(url, item), e))
                        except Exception as e:
                            self.logger.exception(hcpup.log.dpprint(
                                'PUT {} ({}) failed - hint:'
                                    .format(url, item), e))
                        else:
                            if con.response_status != 201:
                                self.logger.warning('PUT {} ({}) failed - {}-{}'
                                                    .format(url, item,
                                                            con.response_status,
                                                            con.response_reason)
                                                    )
                            else:
                                if self.conf['log uploaded files'] and \
                                                self.logger.getEffectiveLevel()\
                                                == logging.INFO:
                                    self.logger.info('uploaded {} to {} '
                                                     '({:0.3f} secs.)'
                                                     .format(item, url,
                                                             con.service_time2))
                                self.logger.debug('PUT {} ({}) succeeded '
                                                  '({:0.3f} secs.)'
                                                  .format(url, item,
                                                          con.service_time2))

                                if not self.conf['obfuscate']:
                                    if self.conf['delete after upload']:
                                        try:
                                            unlink(item)
                                        except Exception as e:
                                            self.logger.warning(
                                                'failed to unlink {}'
                                                    .format(item))
                                        else:
                                            self.logger.debug(
                                                'successfully unlinked {}'
                                                    .format(item))
                                    continue

                                try:
                                    con.PUT(url, body=annotation,
                                            params={'type': 'custom-metadata',
                                                    'annotation': self.conf[
                                                        'annotation']})
                                except hcpsdk.HcpsdkError as e:
                                    self.logger.warning(hcpup.log.dpprint(
                                            'PUT annotation for{} ({}) failed'
                                            '- hint:'.format(url, item), e))
                                except Exception as e:
                                    self.logger.exception(hcpup.log.dpprint(
                                        'PUT annotation for {} ({}) failed - '
                                        'hint:'.format(url, item), e))
                                else:
                                    if con.response_status != 201:
                                        self.logger.warning(
                                            'PUT annotation for{} ({}) failed -'
                                            ' {}-{}'
                                            .format(url, item,
                                                    con.response_status,
                                                    con.response_reason))
                                    else:
                                        self.logger.debug(
                                            'PUT annotation for {} ({}) '
                                            'succeeded'
                                                .format(url, item))

                                        if self.conf['delete after upload']:
                                            try:
                                                unlink(item)
                                            except Exception as e:
                                                self.logger.warning(
                                                    'failed to unlink {} - {}'
                                                        .format(item, e))
                                            else:
                                                self.logger.debug(
                                                    'successfully unlinked {}'
                                                        .format(item))

                                                # try to delete the folder as well...
                                                if self.conf['remove empty ' \
                                                             'folders after ' \
                                                             'upload']:
                                                    self.rmfolder(item)


                except Exception as f:
                    self.logger.debug('upload of {} failed...\n\thint: {}'
                                      .format(item, f))

        except Exception as e:
            self.logger.exception(
                'Uploader failed!!!')

    def fixannotation(self, item, annotation):
        """
        Fix the annotation by adding additional attributes.

        :param item:        the file picked from the queue
        :param annotation:  the annotation from hcpsdk.pathbuilder
        :return:            the new annotation
        """
        root = ET.fromstring(annotation)
        if self.conf['tag_timestamp']:
            root.set('timestamp', str(int(stat(item).st_ctime)))
        root.set('note', self.conf['tag_note'])

        et = ET.ElementTree(element=root)
        with BytesIO() as xmlstring:
            et.write(xmlstring, encoding="utf-8", method="xml",
                     xml_declaration=True)
            annotation = xmlstring.getvalue().decode()
            self.logger.debug(hcpup.log.dpprint('annotation:', annotation))

        return annotation

    def rmfolder(self, item):
        """
        Try to remove a path up to watchdir.

        :param item: the path/filename to which the path shall be removed
        """
        while True:
            item = dirname(item)
            if item == self.conf['watchdir']:
                break

            try:
                self.logger.debug(hcpup.log.dpprint('WatchManager content:',
                                                    self.queues.watchmgr.watches))
                rmdir(item)
                time.sleep(.5)
                self.logger.debug(hcpup.log.dpprint('WatchManager content:',
                                                    self.queues.watchmgr.watches))
            except OSError:
                pass
            else:
                if item in self.queues.doubledirs.keys():
                    del self.queues.doubledirs[item]
                self.logger.debug('successfully removed dir {}'.format(item))


