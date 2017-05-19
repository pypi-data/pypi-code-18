"""byte - executor database cursor module."""
from __future__ import absolute_import, division, print_function


class DatabaseCursor(object):
    """Database cursor class."""

    def __init__(self, executor, connection=None):
        """Create database cursor.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor

        :param connection: Connection
        :type connection: byte.executors.core.models.database.connection.Connection or None
        """
        self.executor = executor
        self.connection = connection

        # Retrieve connection (if not provided)
        if not self.connection:
            self.connection = self.executor.connection()

        # Acquire connection
        self.connection.acquire()

    def execute(self, *args, **kwargs):
        """Execute statement."""
        raise NotImplementedError

    def close(self):
        """Close cursor."""
        # Release connection
        self.connection.release()
        self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
