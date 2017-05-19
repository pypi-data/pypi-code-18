# -*- coding: utf-8 -*-

"""byte - collection module."""

from __future__ import absolute_import, division, print_function

from byte.core.compat import PY26
from byte.core.plugin.manager import PluginManager
from byte.executors.core.base import Executor, FormatExecutor
from byte.model import Model
from byte.queries import DeleteQuery, InsertQuery, SelectQuery, UpdateQuery

from six import string_types
from six.moves.urllib.parse import ParseResult, parse_qsl, urlparse
import inspect
import logging

log = logging.getLogger(__name__)


class CollectionError(Exception):
    """Generic collection error."""


class CollectionLoadError(CollectionError):
    """Collection couldn't be loaded."""


class CollectionModelError(CollectionError):
    """Collection model violation."""


class CollectionParseError(CollectionError):
    """Collection parse error."""


class CollectionValidationError(CollectionError):
    """Collection item violation error."""


class Collection(object):
    """Collection for the storage of keyed items."""

    def __init__(self, model_or_uri=None, uri=None, model=None, executor=None, plugins=None, **kwargs):
        """
        Create keyed item collection.

        :param uri: Data Source URI
        :type uri: str

        :param model: Collection data model
        :type model: class

        :param executor: Collection executor
        :type executor: byte.executors.core.base.Executor or type

        :param plugins: List of plugins to enable for the collection (if :code:`None` is provided
                        all plugins will be enabled)
        :type plugins: list
        """
        self.model = None

        self.uri = None
        self.parameters = {}

        self._executor = None
        self._executor_cls = None

        self.plugins = None

        # Parse `model_or_uri` parameter
        model, uri = self._resolve_model_or_uri(model_or_uri, model, uri)

        # Parse keyword parameters
        if model:
            self.model = model

        # Construct plugin manager
        self.plugins = PluginManager(plugins)

        # Parse URI
        self._parse_uri(uri)

        # Retrieve executor
        if executor:
            self.executor = executor
        elif uri:
            self.executor = self.plugins.get_executor_by_scheme(self.uri.scheme)

        # Set plugin configuration
        self._configure_plugins(**kwargs)

    @property
    def executor(self):
        """Retrieve collection executor.

        :return: Executor
        :rtype: byte.executors.core.base.Executor
        """
        if not self._executor:
            # Ensure executor class is available
            if not self._executor_cls:
                raise CollectionLoadError('No executor available')

            # Construct executor instance
            self._executor = self._executor_cls(
                self,
                self.model
            )

        # Return current executor instance
        return self._executor

    @executor.setter
    def executor(self, value):
        """Set the current collection executor.

        :param value: Executor (class or instance)
        :type value: byte.executors.core.base.Executor or class
        """
        if not value:
            self._executor = None
            self._executor_cls = None
            return

        # Class
        if inspect.isclass(value) and issubclass(value, Executor):
            self._executor = None
            self._executor_cls = value
            return

        # Instance
        if isinstance(value, Executor):
            self._executor = value
            self._executor_cls = None

        # Unknown value
        raise ValueError('Unknown value provided (expected `Executor` class or instance)')

    @property
    def format(self):
        """Retrieve collection executor format."""
        if not isinstance(self.executor, FormatExecutor):
            raise ValueError('Executor doesn\'t support formats')

        return self.executor.format

    @property
    def internal(self):
        """Retrieve internal model metadata."""
        if not self.model:
            return None

        return self.model.Internal

    @property
    def properties(self):
        """Retrieve model properties."""
        if not self.model:
            return None

        return self.model.Properties

    def bind(self, model):
        """Bind collection to data model.

        :param model: Data model
        :type model: byte.model.Model
        """
        if not model or not issubclass(model, Model):
            raise CollectionModelError('Invalid value provided for the "model" parameter (expected Model subclass)')

        self.model = model

    def connect(self, prop, collection):
        """Connect collection to relation property.

        :param prop: Relation property
        :type prop: byte.property.RelationProperty

        :param collection: Collection
        :type collection: Collection
        """
        if not prop:
            raise ValueError('Invalid property')

        prop.connect(collection)

    def transaction(self):
        """Create transaction.

        :return: Transaction
        :rtype: byte.executors.core.models.database.transaction.DatabaseTransaction
        """
        if not self.executor:
            raise Exception('No executor available')

        transaction = self.executor.transaction()

        if transaction.operations > 0:
            raise Exception('Transaction is already active')

        return transaction

    def execute(self, query):
        """Execute query.

        :param query: Query
        :type query: byte.queries.Query
        """
        if not self.executor:
            raise Exception('No executor available')

        return self.executor.execute(query)

    def all(self):
        """Retrieve all items from collection."""
        return self.select()

    def delete(self):
        """Create delete query."""
        return DeleteQuery(self, self.model)

    def select(self, *properties):
        """Create select query."""
        return SelectQuery(
            self, self.model,
            properties=properties or None
        )

    def update(self, args, **kwargs):
        """Create update query."""
        data = kwargs

        for value in args:
            data.update(value)

        return UpdateQuery(
            self, self.model,
            data=data
        )

    def create(self, **kwargs):
        """Create item."""
        if not self.model:
            raise Exception('Collection has no model bound')

        return self.model.create(
            _collection=self,
            **kwargs
        )

    def create_or_get(self):
        """Create (or retrieve the existing) item."""
        raise NotImplementedError

    # TODO Better handling of primary key queries (string values are currently parsed as expressions)
    def get(self, *expressions, **kwargs):
        """Retrieve item."""
        query = self.select().limit(1)

        if expressions:
            query = query.where(*expressions)

        if kwargs:
            query = query.filter(**kwargs)

        return query.first()

    def get_or_create(self):
        """Retrieve existing (or create) item."""
        raise NotImplementedError

    def insert(self, *args):
        """Create insert query."""
        return InsertQuery(
            self, self.model,
            properties=args or None
        )

    def insert_from(self, query, properties):
        """Create insert from query."""
        return InsertQuery(
            self, self.model,
            query=query,
            properties=properties
        )

    def insert_many(self, items):
        """Create insert many query."""
        return InsertQuery(
            self, self.model,
            items=items
        )

    def _resolve_model_or_uri(self, model_or_uri, model, uri):
        if not model_or_uri:
            return model, uri

        if inspect.isclass(model_or_uri) and issubclass(model_or_uri, Model):
            model = model_or_uri
        elif isinstance(model_or_uri, string_types):
            uri = model_or_uri
        else:
            raise ValueError('Unknown initialization parameter value (expected subclass of Model, or string)')

        return model, uri

    def _parse_uri(self, uri):
        if not uri:
            return

        if PY26:
            # Retrieve scheme from `uri`
            scheme_end = uri.index('://')
            scheme = uri[0:scheme_end]

            # Replace scheme in `uri` with "http" (to avoid parsing bugs)
            uri = 'http' + uri[scheme_end:]

            # Parse URI
            parsed = urlparse(uri)

            # Build parse result with original scheme
            self.uri = ParseResult(scheme, *parsed[1:])
        else:
            self.uri = urlparse(uri)

        if self.uri.query:
            self.parameters = dict(parse_qsl(self.uri.query))

    def _configure_plugins(self, **kwargs):
        for key, value in kwargs.items():
            kind, key = tuple(key.split('_', 1))

            # Ensure plugin exists
            if not hasattr(self, kind):
                raise ValueError('Unknown plugin: %s' % (kind,))

            # Ensure attribute exists
            plugin = getattr(self, kind)

            if not hasattr(plugin, key):
                raise ValueError('Unknown plugin attribute: %s.%s' % (kind, key))

            # Set attribute value
            setattr(plugin, key, value)


# noinspection PyAbstractClass
class CollectionMixin(Collection):
    """Base class for collection mixins."""
