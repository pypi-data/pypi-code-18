# coding=utf-8
from abc import ABCMeta, abstractmethod

from inginious.services.service import Service
from inginious.services.service_stats import StatsService


class TaskService(Service, metaclass=ABCMeta):
    """ A service that provides 'tasks' in the INGInious sense.
    
        A task service will always provide a method to create a new job, which returns a job_id, which must be unique.
        
        It is also responsible to call the registered StatsService to reflect their internal state at any time.
    """
    def __init__(self, stat_service: StatsService = None):
        self._stat_service = stat_service

    @abstractmethod
    def available_environments(self):
        """ Returns a list of available environments (str ids) """
        pass

    @abstractmethod
    def kill_job(self, job_id):
        """
        Kills a running job
        :param job_id:
        """
        pass
