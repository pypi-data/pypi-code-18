"""Kinesis utilities."""

from collections import namedtuple
import multiprocessing
from queue import Empty
import json
import time

import boto3
from botocore.exceptions import ClientError
from retrying import retry
import wrapt


def retry_if_client_error(exception):
    """Return True if we should retry."""
    return isinstance(exception, ClientError)


client = boto3.client("kinesis")


class KinesisConsumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue, limit):
        multiprocessing.Process.__init__(self)
        self.limit = limit
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            #print("{}: working on {}".format(proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            for rec in answer.records:
                self.result_queue.put(json.loads(rec['Data'].decode()))
            time.sleep(0.1)
            self.task_queue.put(Task(answer.shard_iterator, self.limit))
        return


TaskResponse = namedtuple("TaskResponse", "shard_iterator records")


class Task(object):
    def __init__(self, shard_iter, limit):
        self.shard_iter = shard_iter
        self.limit = limit

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000,
           wrap_exception=True)
    def __call__(self):
        resp = client.get_records(
            ShardIterator=self.shard_iter, Limit=self.limit)
        return TaskResponse(resp["NextShardIterator"], resp["Records"])

    def __str__(self):
        return "{} (limit={})".format(self.shard_iter, self.limit)


class KinesisGenerator(object):

    """Generate records from an AWS Kinesis stream."""

    def __init__(self, stream_name, timeout=60, limit=100, max_consumers=50):
        """Initialize."""

        self.stream_name = stream_name
        self.tasks = multiprocessing.JoinableQueue()
        self.results = multiprocessing.Queue()
        self.limit = limit
        self.timeout = timeout

        num_consumers = min(
            multiprocessing.cpu_count() * 2,
            self.shard_count,
            max_consumers)
        self.consumers = [
            KinesisConsumer(self.tasks, self.results, self.limit)
            for _ in range(num_consumers)]

        for sid in self.get_shard_iterators():
            self.tasks.put(Task(sid, self.limit))


    @property
    def shard_ids(self):
        """Get the shard IDs."""
        res = client.describe_stream(StreamName=self.stream_name)
        return [x['ShardId'] for x in res['StreamDescription']['Shards']]

    @property
    def shard_count(self):
        """The stream shard count."""
        return len(self.shard_ids)

    def get_shard_iterators(self, shard_ids=None, type="LATEST"):
        """Get a list of shard iterators, one per shard in the stream."""
        if shard_ids is None:
            shard_ids = self.shard_ids
        return [client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=sid,
            ShardIteratorType=type)["ShardIterator"] for sid in shard_ids]

    def _start(self):
        """Start the consumers."""
        for c in self.consumers:
            if not c.is_alive():
                c.start()

    def _terminate(self):
        """Terminate the consumers."""
        for c in self.consumers:
            if c.is_alive():
                c.terminate()

    def __iter__(self):
        """Generate records from the Kinesis stream."""
        self._start()
        t0 = time.time()
        while (time.time() - t0) < self.timeout:
            try:
                yield self.results.get(timeout=self.timeout)
            except Empty:
                print("Waited {} seconds for records".format(self.timeout))
                self._terminate()
                return

        print("Time out!")
        self._terminate()
