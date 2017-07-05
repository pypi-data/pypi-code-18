# coding=utf-8
from abc import abstractmethod, ABCMeta

from inginious.services.service import TaskService


class TaskServiceMCQ(TaskService, metaclass=ABCMeta):
    def available_environments(self):
        return ["MCQ"]

    @abstractmethod
    def grade_mcq(self, task, inputdata, callback, launcher_name="Unknown"):
        """ Add a new job. Every callback will be called once and only once.
        :param task: A Task object, whose environment is MCQ.
        :type task: Task
        :param inputdata: input from the student
        :type inputdata: Storage or dict
        :param callback: a function that will be called asynchronously in the client's process, with the results.
            its signature must be (result, grade, problems), where:
            result is itself a tuple containing the result string and the main feedback (i.e. ('success', 'You succeeded');
            grade is a number between 0 and 100 indicating the grade of the users;
            problems is a dict of tuple, in the form {'problemid': result};
        :type callback: __builtin__.function or __builtin__.instancemethod
        :param launcher_name: for informational use
        :type launcher_name: str
        :return: the new job id
        """
        pass
