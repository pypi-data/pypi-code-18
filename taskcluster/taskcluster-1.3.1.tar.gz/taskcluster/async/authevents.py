# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from .asyncclient import AsyncBaseClient
from .asyncclient import createApiClient
from .asyncclient import config
from .asyncclient import createTemporaryCredentials
from .asyncclient import createSession
_defaultConfig = config


class AuthEvents(AsyncBaseClient):
    """
    The auth service, typically available at `auth.taskcluster.net`
    is responsible for storing credentials, managing assignment of scopes,
    and validation of request signatures from other services.

    These exchanges provides notifications when credentials or roles are
    updated. This is mostly so that multiple instances of the auth service
    can purge their caches and synchronize state. But you are of course
    welcome to use these for other purposes, monitoring changes for example.
    """

    classOptions = {
        "exchangePrefix": "exchange/taskcluster-auth/v1/"
    }

    """
    Client Created Messages

    Message that a new client has been created.

    This exchange outputs: ``http://schemas.taskcluster.net/auth/v1/client-message.json#``This exchange takes the following keys:

     * reserved: Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.
    """

    def clientCreated(self, *args, **kwargs):
        return self._makeTopicExchange({'routingKey': [{'required': False, 'multipleWords': True, 'summary': 'Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.', 'name': 'reserved'}], 'name': 'clientCreated', 'schema': 'http://schemas.taskcluster.net/auth/v1/client-message.json#', 'exchange': 'client-created'}, *args, **kwargs)

    """
    Client Updated Messages

    Message that a new client has been updated.

    This exchange outputs: ``http://schemas.taskcluster.net/auth/v1/client-message.json#``This exchange takes the following keys:

     * reserved: Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.
    """

    def clientUpdated(self, *args, **kwargs):
        return self._makeTopicExchange({'routingKey': [{'required': False, 'multipleWords': True, 'summary': 'Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.', 'name': 'reserved'}], 'name': 'clientUpdated', 'schema': 'http://schemas.taskcluster.net/auth/v1/client-message.json#', 'exchange': 'client-updated'}, *args, **kwargs)

    """
    Client Deleted Messages

    Message that a new client has been deleted.

    This exchange outputs: ``http://schemas.taskcluster.net/auth/v1/client-message.json#``This exchange takes the following keys:

     * reserved: Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.
    """

    def clientDeleted(self, *args, **kwargs):
        return self._makeTopicExchange({'routingKey': [{'required': False, 'multipleWords': True, 'summary': 'Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.', 'name': 'reserved'}], 'name': 'clientDeleted', 'schema': 'http://schemas.taskcluster.net/auth/v1/client-message.json#', 'exchange': 'client-deleted'}, *args, **kwargs)

    """
    Role Created Messages

    Message that a new role has been created.

    This exchange outputs: ``http://schemas.taskcluster.net/auth/v1/role-message.json#``This exchange takes the following keys:

     * reserved: Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.
    """

    def roleCreated(self, *args, **kwargs):
        return self._makeTopicExchange({'routingKey': [{'required': False, 'multipleWords': True, 'summary': 'Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.', 'name': 'reserved'}], 'name': 'roleCreated', 'schema': 'http://schemas.taskcluster.net/auth/v1/role-message.json#', 'exchange': 'role-created'}, *args, **kwargs)

    """
    Role Updated Messages

    Message that a new role has been updated.

    This exchange outputs: ``http://schemas.taskcluster.net/auth/v1/role-message.json#``This exchange takes the following keys:

     * reserved: Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.
    """

    def roleUpdated(self, *args, **kwargs):
        return self._makeTopicExchange({'routingKey': [{'required': False, 'multipleWords': True, 'summary': 'Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.', 'name': 'reserved'}], 'name': 'roleUpdated', 'schema': 'http://schemas.taskcluster.net/auth/v1/role-message.json#', 'exchange': 'role-updated'}, *args, **kwargs)

    """
    Role Deleted Messages

    Message that a new role has been deleted.

    This exchange outputs: ``http://schemas.taskcluster.net/auth/v1/role-message.json#``This exchange takes the following keys:

     * reserved: Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.
    """

    def roleDeleted(self, *args, **kwargs):
        return self._makeTopicExchange({'routingKey': [{'required': False, 'multipleWords': True, 'summary': 'Space reserved for future routing-key entries, you should always match this entry with `#`. As automatically done by our tooling, if not specified.', 'name': 'reserved'}], 'name': 'roleDeleted', 'schema': 'http://schemas.taskcluster.net/auth/v1/role-message.json#', 'exchange': 'role-deleted'}, *args, **kwargs)

    funcinfo = {
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'AuthEvents']
