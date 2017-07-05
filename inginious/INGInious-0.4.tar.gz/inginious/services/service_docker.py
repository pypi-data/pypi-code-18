# coding=utf-8
from abc import abstractmethod, ABCMeta

from inginious.services.service import TaskService


class TaskServiceDocker(TaskService, metaclass=ABCMeta):
    @abstractmethod
    def grade_docker(self, task, inputdata, callback, launcher_name="Unknown", debug=False, ssh_callback=None):
        """ Add a new job. Every callback will be called once and only once.
        :param task: a Task object, whose environment must be one provided by the current service.
        :type task: Task
        :param inputdata: input from the student
        :type inputdata: Storage or dict
        :param callback: a function that will be called asynchronously in the client's process, with the results.
            it's signature must be (result, grade, problems, tests, custom, archive), where:
            result is itself a tuple containing the result string and the main feedback (i.e. ('success', 'You succeeded');
            grade is a number between 0 and 100 indicating the grade of the users;
            problems is a dict of tuple, in the form {'problemid': result};
            test is a dict of tests made in the container
            custom is a dict containing random things set in the container
            archive is either None or a bytes containing a tgz archive of files from the job
        :type callback: __builtin__.function or __builtin__.instancemethod
        :param launcher_name: for informational use
        :type launcher_name: str
        :param debug: Either True(outputs more info), False(default), or "ssh" (starts a remote ssh server. ssh_callback needs to be defined)
        :type debug: bool or string
        :param ssh_callback: a callback function that will be called with (host, port, password), the needed credentials to connect to the
                             remote ssh server. May be called with host, port, password being None, meaning no session was open.
        :type ssh_callback: __builtin__.function or __builtin__.instancemethod or None
        :return: the new job id
        """
        pass
