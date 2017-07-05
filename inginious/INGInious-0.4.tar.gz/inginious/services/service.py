# coding=utf-8
from abc import ABCMeta, abstractmethod


class Service(object, metaclass=ABCMeta):
    """ Basis for any INGInious service """

    @abstractmethod
    def start(self):
        """ Starts the service. Should be done after a complete initialisation of the hook manager. """
        pass

    @abstractmethod
    def close(self):
        """ Close the service """
        pass


class TaskService(Service, metaclass=ABCMeta):
    """ A service that provides 'tasks' in the INGInious sense """
