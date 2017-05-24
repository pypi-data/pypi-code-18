#!/usr/lib/env python
# -*- encoding:utf-8 -*-


class QueueJobTracker(object):
    """
        顺序工作
    """
    def __init__(self):
        self.workers = []
        self.context = {}


    def publish_task(self, task):
        """
            发布工作
        """
        for worker in workers:
            worker.execute(self.context, task)


    def register_worker(self, worker):
        """
            添加工人
        """
        self.workers.append(worker)


class SwichJobTracker(object):
    """
        岗位工作
    """
    def __init__(self):
        self.workers = {}


    def publish_task(self, code, task):
        """
            发布工作
        """
        worker = self.workers.get(code)
        if worker:
            worker.execute(task)


    def register_worker(self, code, worker):
        """
            添加工人
        """
        self.workers[code] = worker
