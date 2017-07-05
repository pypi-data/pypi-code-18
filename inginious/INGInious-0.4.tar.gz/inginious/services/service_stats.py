# coding=utf-8
from abc import abstractmethod, ABCMeta

from inginious.services.service import Service

class StatsService(Service, metaclass=ABCMeta):
    @abstractmethod
    def get_job_queue_snapshot(self):
        """ Get a snapshot of the remote backend job queue. May be a cached version.
            May not contain recent jobs. May return None if no snapshot is available

        Return a tuple of two lists (or None, None):
        jobs_running: a list of tuples in the form
            (job_id, is_current_client_job, is_batch, info, launcher, started_at, max_end)
            where
            - job_id is a job id. It may be from another client.
            - is_current_client_job is a boolean indicating if the client that asked the request has started the job
            - agent_name is the agent name
            - is_batch is True if the job is a batch job, false else
            - info is either the batch container name if is_batch is True, or "courseid/taskid"
            - launcher is the name of the launcher, which may be anything
            - started_at the time (in seconds since UNIX epoch) at which the job started
            - max_end the time at which the job will timeout (in seconds since UNIX epoch), or -1 if no timeout is set
        jobs_waiting: a list of tuples in the form
            (job_id, is_current_client_job, is_batch, info, launcher, max_time)
            where
            - job_id is a job id. It may be from another client.
            - is_current_client_job is a boolean indicating if the client that asked the request has started the job
            - is_batch is True if the job is a batch job, false else
            - info is either the batch container name if is_batch is True, or "courseid/taskid"
            - launcher is the name of the launcher, which may be anything
            - max_time the maximum time that can be used, or -1 if no timeout is set
        """
        pass

    @abstractmethod
    def get_job_queue_info(self, jobid):
        """
        :param jobid: the jobid of a *task*.
        :return: If the submission is in the queue, then returns a tuple (nb tasks before running (or -1 if running), approx wait time in seconds)
                 Else, returns None
        """
        pass
