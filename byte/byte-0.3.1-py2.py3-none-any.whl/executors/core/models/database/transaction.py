"""byte - executor database transaction model module."""
from __future__ import absolute_import, division, print_function

from byte.core.models.threading.local import LocalItem, LocalManager
from byte.executors.core.models.database.cursor import DatabaseCursor

from threading import RLock
import six
import sys

try:
    from thread import get_ident
except ImportError:
    from threading import get_ident


class States(object):
    """Database transaction states."""

    Created = 0

    Starting = 10
    Started = 11

    Finished = 20
    Error = 21


class DatabaseTransaction(DatabaseCursor, LocalItem):
    """Database transaction class."""

    State = States

    def __init__(self, executor, connection=None):
        """Create database transaction.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        super(DatabaseTransaction, self).__init__(
            executor,
            connection=connection
        )

        self._state = States.Created

        self._operations = 0
        self._operation_lock = RLock()

    #
    # Properties
    #

    @property
    def operations(self):
        """Retrieve number of active operations."""
        return self._operations

    @property
    def state(self):
        """Retrieve current state."""
        return self._state

    @property
    def starting(self):
        """Retrieve boolean representing the "starting" state."""
        return self.state == States.Starting

    @property
    def started(self):
        """Retrieve boolean representing the "started" state."""
        return self.state >= States.Started

    @property
    def finished(self):
        """Retrieve boolean representing the "finished" state."""
        return self.state >= States.Finished

    #
    # Public methods
    #

    def acquire(self):
        """Acquire transaction operation lock."""
        if get_ident() != self._ident:
            raise Exception('Connection is in use by another thread')

        with self._operation_lock:
            self._operations += 1

    def close(self):
        """Close transaction."""
        # Commit transaction (if transaction is still active)
        if not self.finished:
            self._commit()

        # Release connection
        self.connection.release()
        self.connection = None

    def release(self):
        """Release transaction operation lock."""
        if get_ident() != self._ident:
            raise Exception('Connection is in use by another thread')

        with self._operation_lock:
            self._operations -= 1

            # End transaction when there are no active operations
            if self._operations < 1:
                self._end()

    #
    # Abstract methods
    #

    def begin(self):
        """Begin transaction."""
        raise NotImplementedError

    def commit(self):
        """Commit transaction."""
        raise NotImplementedError

    def rollback(self):
        """Rollback transaction."""
        raise NotImplementedError

    #
    # Private methods
    #

    def _begin(self):
        if self.starting:
            raise Exception('Transaction is already starting')

        if self.started:
            raise Exception('Transaction has already been started')

        # Update state
        self._state = States.Starting

        # Try start transaction
        try:
            # Begin transaction
            self.begin()

            # Update state
            self._state = States.Started
        except Exception:
            exc_info = sys.exc_info()

            # Update state
            self._state = States.Error

            # Raise exception
            six.reraise(*exc_info)

    def _end(self):
        # Close transaction
        self.close()

        # Detach transaction from thread
        self.detach()

    def _commit(self):
        if self.finished:
            raise Exception('Transaction has already finished')

        # Commit transaction
        self.commit()

        # Update state
        self._state = States.Finished

    def _rollback(self):
        if self.finished:
            raise Exception('Transaction has already finished')

        # Commit transaction
        self.rollback()

        # Update state
        self._state = States.Finished

    #
    # Magic methods
    #

    def __enter__(self):
        # Ensure transaction has been started
        if not self.started:
            self._begin()

        # Acquire transaction
        self.acquire()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Rollback transaction (if transaction is still active)
        if not self.finished and exc_type:
            self._rollback()

        # Release transaction
        self.release()


class DatabaseTransactionManager(LocalManager):
    """Database transaction manager class."""

    def __init__(self, executor):
        """Create database transaction manager.

        :param executor: Executor
        :type executor: byte.executors.core.base.Executor
        """
        super(DatabaseTransactionManager, self).__init__()

        self.executor = executor

    def create(self, **kwargs):
        """Create transaction.

        ;return: Transaction
        :rtype: DatabaseTransaction
        """
        return self.executor.create_transaction(**kwargs)
