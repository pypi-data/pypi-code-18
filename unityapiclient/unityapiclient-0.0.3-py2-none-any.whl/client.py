"""Client for the Unity IDM APIs.

The client provides methods for interacting with the Administration API of a Unity IDM server.

Client instantiation requires specifying the server's base URL and optionally, the deployment path of the endpoint and API version (currently there is only one).
"""

import logging
import requests

from datetime import datetime
from pytz import timezone
import pytz

logger = logging.getLogger(__name__)

DEFAULT_REST_ADMIN_PATH = 'rest-admin'
DEFAULT_API_VERSION = 'v1'
DEFAULT_CERT_VERIFY = True


class UnityApiClient:

    # Thursday, 1 January 1970, 00:00:00 UTC
    _EPOCH = datetime(1970, 1, 1, tzinfo=pytz.utc)

    def __init__(self, server_base_url, **kwargs):
        """Constructs a new :class:`UnityApiClient <UnityApiClient>`.

        :param server_base_url: base URL of the Unity IDM server.
        :param rest_admin_path: API endpoint path. Defaults to 
            `rest-admin`.
        :param api_version: API version. Defaults to `v1`.
        :param auth: (optional) Auth tuple to enable HTTP Auth.
        :param cert_verify: (optional) whether the server SSL cert
            will be verified. A CA_BUNDLE path can also be provided. 
            Defaults to ``True``.
        """

        self.__session = requests.Session()
        if 'auth' in kwargs:
            self.__session.auth = kwargs['auth']
        self.__session.verify = kwargs.setdefault('cert_verify', 
            DEFAULT_CERT_VERIFY)
        self.__api_base_url = self._build_api_base_url(
            server_base_url,
            kwargs.setdefault('rest_admin_path', DEFAULT_REST_ADMIN_PATH),
            kwargs.setdefault('api_version', DEFAULT_API_VERSION))

    def get_group(self, group_path=None):
        """Returns all members and subgroups of the specified group.

        If ``group_path`` is not supplied, then the method returns all
        root-level groups and members. 

        @param group_path: (optional) path to group whose subgroups
            and members to retrieve. 

        Example response::

             {
               "subGroups" : [ ],
               "members" : [ 3 ]
             }

        """
        if group_path is not None:
            path = '/group/' + group_path
        else:
            path = '/group/%2F'
        try:
            response = self.__session.get(self.__api_base_url + path)
            response.raise_for_status()
            response = response.json()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

        return response

    def get_entity(self, entity_id):
        """Returns information about the identified entity, including
        its status and all identities.

        @param entity_id: numeric identifier of the entity whose status
            and identities to retrieve.

        Example response::

             {
               "id" : 3,
               "state" : "valid",
               "identities" : [ {
                 "typeId" : "userName",
                 "value" : "tested",
                 "target" : null,
                 "realm" : null,
                 "local" : true,
                 "entityId" : 3,
                 "comparableValue" : "tested"
               }, {
                 "typeId" : "persistent",
                 "value" : "129ffe63-63b9-4467-ae24-6bc889327b0d",
                 "target" : null,
                 "realm" : null,
                 "local" : true,
                 "entityId" : 3,
                 "comparableValue" : "129ffe63-63b9-4467-ae24-6bc889327b0d"
               } ],
               "credentialInfo" : {
                 "credentialRequirementId" : "cr-pass",
                 "credentialsState" : {
                   "credential1" : {
                     "state" : "notSet",
                     "extraInformation" : ""
                   }
                 }
               }
             }

        """
        path = '/entity/' + str(entity_id)
        try:
            response = self.__session.get(self.__api_base_url + path)
            response.raise_for_status()
            response = response.json()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

        return response

    def get_entity_groups(self, entity_id):
        """Returns all groups of the identified entity.

        @param entity_id: numeric identifier of the entity whose groups to 
            retrieve.

        Example response::

             ["/example/sub","/example","/"]

        """
        path = '/entity/' + str(entity_id) + '/groups'
        try:
            response = self.__session.get(self.__api_base_url + path)
            response.raise_for_status()
            response = response.json()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

        return response

    def get_entity_attrs(self, entity_id, group_path=None, 
                              effective=True):
        """Returns all attributes of the identified entity.

        If ``group_path`` is not supplied, then the method returns the 
        attributes in all groups the entity is member of. 

        @param entity_id: numeric identifier of the entity whose attributes to 
            retrieve.
        @param group_path: (optional) path to the group associated with the 
            attributes to retrieve.
        @param effective: (optional) whether to retrieve only directly defined
            or effective attributes (by default True).

        Example response::

            [ 
              {
                "values" : [ "/9j/4AAQSk .... KKKKACiiigD//2Q==" ],
                "direct" : true,
                "name" : "jpegA",
                "groupPath" : "/example",
                "visibility" : "full",
                "syntax" : "jpegImage"
              }, 
              {
                "values" : [ "value" ],
                "direct" : true,
                "name" : "stringA",
                "groupPath" : "/example",
                "visibility" : "full",
                "syntax" : "string"
              } 
            ]

        """
        path = '/entity/' + str(entity_id) + '/attributes'
        params = {'effective': effective}
        if group_path is not None:
            params['group'] = group_path
        try:
            response = self.__session.get(self.__api_base_url + path, 
                                          params=params)
            response.raise_for_status()
            response = response.json()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

        return response

    def remove_entity_attr(self, entity_id, attr_name):
        """Removes the given attribute of the identified entity.

        @param entity_id: numeric identifier of the entity whose attribute
            to remove
        @param attr_name: name of the attribute to remove

        """
        path = '/entity/' + str(entity_id) + '/attribute/' + str(attr_name)
        try:
            response = self.__session.delete(self.__api_base_url + path)
            response.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

    def schedule_operation(self, entity_id, operation, when=None,
                           identity_type=None):
        """Schedules an operation to be invoked at a given time on the
        identified entity. Allowed operations are: 'REMOVE' and
        'DISABLE'.

        Important: This method requires a privileged user.

        @param entity_id: numeric identifier of the entity for which to
            schedule the operation.
        @param operation: operation to be scheduled. Allowed operations
            are: 'REMOVE' and 'DISABLE'.
        @parm when: (optional) datetime when to invoke the operation
            (default is now). Naive datetime instances assume UTC time.
        @param identity_type: (optional) type of identity for which to
            schedule the operation.

        """
        if operation not in ['REMOVE', 'DISABLE']:
            raise ValueError('Unknown operation: %r' % operation)
        path = '/entity/' + str(entity_id) + '/admin-schedule'
        params = {'operation': operation}
        if when is not None:
            if not isinstance(when, datetime):
                raise TypeError("when argument must be an instance of datetime")
            params['when'] = self._time_ms(when)
        if identity_type is not None:
            params['identityType'] = identity_type
        try:
            response = self.__session.put(self.__api_base_url + path,
                                          params=params)
            response.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

    def _build_api_base_url(self,
        server_base_url, 
        rest_admin_path, 
        api_version):
        
        return '{0}/{1}/{2}'.format(server_base_url, 
                                    rest_admin_path, 
                                    api_version) 

    def _time_ms(self, dt):
        """Returns the number of milliseconds since the epoch for the
        specified datetime"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.utc)
        return int((dt - self._EPOCH).total_seconds() * 1000)
