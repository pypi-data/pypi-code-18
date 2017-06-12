# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import threading
import importlib
import traceback
import logging

try:
    # noinspection PyCompatibility
    from Queue import Queue
except ImportError:
    # noinspection PyUnresolvedReferences
    from queue import Queue

__all__ = ['start_workers']

log = logging.getLogger(__name__)


def start_workers(num_threads):
    queue = Queue()
    for i in range(num_threads):
        name = 'MetricsThread-' + str(i + 1)
        t = MetricsThread(name=name, target=None, args=(queue,), kwargs={})
        t.start()
    return queue


class MetricsThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        super(MetricsThread, self).__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)
        self.args = args
        self.kwargs = kwargs if kwargs is not None else {}
        self.daemon = True

    def run(self):
        # called by start() method, thread is considered "alive" until run() method terminates
        log.debug('running')
        queue = self.args[0]
        while True:
            try:
                # block until we get an item
                item = queue.get(True, None)
                log.debug('got item from queue: %s' % item)
                self.do_work(item)
            except:
                log.error('exception:\n%s' % traceback.format_exc())
            # call task_done() here so queue.join() returns, even though an exception may have been thrown;
            # if we tried to add item back to queue on exception, we may never complete due to recurring exception
            queue.task_done()

    def do_work(self, item):
        config = item['config']
        timestamp = item['timestamp']
        plugin = item['plugin']

        if plugin['config'].get('plugin_import'):
            plugin_modname = plugin['config'].get('plugin_import')
        else:
            plugin_modname = 'timera.plugins.' + plugin['type']

        try:
            plugin_modref = importlib.import_module(plugin_modname)
        except:
            raise ImportError('exception importing plugin module "%s":\n%s' % (plugin_modname, traceback.format_exc()))
        else:
            get_metrics = getattr(plugin_modref, 'get_metrics')

        get_metrics(config, timestamp, plugin)
