"""byte - executor database connection module."""
from __future__ import absolute_import, division, print_function

from byte.core.models.threading.pool import PoolItem, PoolManager

from threading import RLock

try:
    from thread import get_ident
except ImportError:
    from threading import get_ident


class DatabaseConnection(PoolItem):
    """Database connection class."""

    def __init__(self, executor):
        """Create database connection.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        super(DatabaseConnection, self).__init__()

        self.executor = executor

        self._operations = 0
        self._operation_lock = RLock()

    #
    # Properties
    #

    @property
    def operations(self):
        """Retrieve number of active operations."""
        return self._operations

    #
    # Public methods
    #

    def acquire(self):
        """Acquire connection operation lock."""
        if self._manager is None:
            return

        if get_ident() != self._ident:
            raise Exception('Connection is in use by another thread')

        with self._operation_lock:
            self._operations += 1

    def cursor(self):
        """Create cursor.

        :return: Cursor
        :rtype: byte.executors.core.models.database.cursor.DatabaseCursor
        """
        return self.executor.cursor(
            connection=self
        )

    def execute(self, *args, **kwargs):
        """Execute statement, and return the cursor.

        :return: Cursor
        :rtype: byte.executors.core.models.database.cursor.DatabaseCursor
        """
        cursor = self.cursor()
        cursor.execute(*args, **kwargs)

        return cursor

    def release(self):
        """Release connection operation lock."""
        if self._manager is None:
            return

        if get_ident() != self._ident:
            raise Exception('Connection is in use by another thread')

        with self._operation_lock:
            self._operations -= 1

            # Detach connection when there are no active operations
            if self._operations < 1:
                self.detach()

    def transaction(self):
        """Create transaction.

        :return: Transaction
        :rtype: byte.executors.core.models.database.transaction.DatabaseTransaction
        """
        return self.executor.transaction(
            connection=self
        )

    #
    # Abstract methods
    #

    def close(self):
        """Close connection, and remove it from the pool."""
        raise NotImplementedError

    #
    # Magic methods
    #

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Detach connection
        self.detach()


class DatabaseConnectionPool(PoolManager):
    """Database connection pool class."""

    def __init__(self, executor):
        """Create database connection pool.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        super(DatabaseConnectionPool, self).__init__()

        self.executor = executor

    def create(self, **kwargs):
        """Create connection.

        ;return: Connection
        :rtype: DatabaseConnection
        """
        return self.executor.create_connection(**kwargs)
