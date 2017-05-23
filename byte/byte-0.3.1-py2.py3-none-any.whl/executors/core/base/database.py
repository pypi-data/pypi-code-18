"""byte - base database executor module."""

from __future__ import absolute_import, division, print_function

from byte.executors.core.base.executor import Executor, ExecutorPlugin
from byte.executors.core.models.database import DatabaseConnectionPool, DatabaseTransactionManager


class DatabaseExecutor(Executor):
    """Base database executor class."""

    def __init__(self, collection, model):
        """Create database executor.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model
        """
        super(DatabaseExecutor, self).__init__(collection, model)

        self.connections = DatabaseConnectionPool(self)
        self.transactions = DatabaseTransactionManager(self)

    #
    # Public methods
    #

    def connection(self, blocking=False, **kwargs):
        """Create (or retrieve the current) connection.

        :return: Connection
        :rtype: byte.executors.core.models.database.connection.DatabaseConnection
        """
        return self.connections.get(
            blocking=blocking,
            **kwargs
        )

    def transaction(self, **kwargs):
        """Create (or retrieve the current) transaction.

        :return: Transaction
        :rtype: byte.executors.core.models.database.transaction.DatabaseTransaction
        """
        return self.transactions.get(
            **kwargs
        )

    #
    # Abstract methods
    #

    def create_connection(self, **kwargs):
        """Create database connection.

        :return: Connection
        :rtype: byte.executors.core.models.database.connection.DatabaseConnection
        """
        raise NotImplementedError

    def create_transaction(self, **kwargs):
        """Create database transaction.

        :return: Transaction
        :rtype: byte.executors.core.models.database.transaction.DatabaseTransaction
        """
        raise NotImplementedError


class DatabaseExecutorPlugin(DatabaseExecutor, ExecutorPlugin):
    """Base database executor plugin class."""

    pass
