# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from twilio.instance_context import InstanceContext
from twilio.instance_resource import InstanceResource
from twilio.list_resource import ListResource
from twilio.rest.notifications.v1.service.binding import BindingList
from twilio.rest.notifications.v1.service.notification import NotificationList

from twilio import values
from twilio.base import deserialize, values
from twilio.base.page import Page


class ServiceList(ListResource):

    def __init__(self, version):
        """
        Initialize the ServiceList
        
        :param Version version: Version that contains the resource
        
        :returns: ServiceList
        :rtype: ServiceList
        """
        super(ServiceList, self).__init__(version)
        
        # Path Solution
        self._solution = {}
        self._uri = '/Services'.format(**self._solution)

    def create(self, friendly_name=values.unset, apn_credential_sid=values.unset,
               gcm_credential_sid=values.unset, messaging_service_sid=values.unset,
               facebook_messenger_page_id=values.unset,
               default_apn_notification_protocol_version=values.unset,
               default_gcm_notification_protocol_version=values.unset):
        """
        Create a new ServiceInstance
        
        :param unicode friendly_name: The friendly_name
        :param unicode apn_credential_sid: The apn_credential_sid
        :param unicode gcm_credential_sid: The gcm_credential_sid
        :param unicode messaging_service_sid: The messaging_service_sid
        :param unicode facebook_messenger_page_id: The facebook_messenger_page_id
        :param unicode default_apn_notification_protocol_version: The default_apn_notification_protocol_version
        :param unicode default_gcm_notification_protocol_version: The default_gcm_notification_protocol_version
        
        :returns: Newly created ServiceInstance
        :rtype: ServiceInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'ApnCredentialSid': apn_credential_sid,
            'GcmCredentialSid': gcm_credential_sid,
            'MessagingServiceSid': messaging_service_sid,
            'FacebookMessengerPageId': facebook_messenger_page_id,
            'DefaultApnNotificationProtocolVersion': default_apn_notification_protocol_version,
            'DefaultGcmNotificationProtocolVersion': default_gcm_notification_protocol_version,
        })
        
        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )
        
        return ServiceInstance(
            self._version,
            payload,
        )

    def stream(self, friendly_name=values.unset, limit=None, page_size=None):
        """
        Streams ServiceInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.
        
        :param unicode friendly_name: The friendly_name
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)
        
        :returns: Generator that will yield up to limit results
        :rtype: generator
        """
        limits = self._version.read_limits(limit, page_size)
        
        page = self.page(
            friendly_name=friendly_name,
            page_size=limits['page_size'],
        )
        
        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, friendly_name=values.unset, limit=None, page_size=None):
        """
        Lists ServiceInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.
        
        :param unicode friendly_name: The friendly_name
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)
        
        :returns: Generator that will yield up to limit results
        :rtype: generator
        """
        return list(self.stream(
            friendly_name=friendly_name,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, friendly_name=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of ServiceInstance records from the API.
        Request is executed immediately
        
        :param unicode friendly_name: The friendly_name
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of ServiceInstance
        :rtype: Page
        """
        params = values.of({
            'FriendlyName': friendly_name,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })
        
        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )
        
        return ServicePage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a ServiceContext
        
        :param sid: The sid
        
        :returns: ServiceContext
        :rtype: ServiceContext
        """
        return ServiceContext(
            self._version,
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a ServiceContext
        
        :param sid: The sid
        
        :returns: ServiceContext
        :rtype: ServiceContext
        """
        return ServiceContext(
            self._version,
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Notifications.V1.ServiceList>'


class ServicePage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the ServicePage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        
        :returns: ServicePage
        :rtype: ServicePage
        """
        super(ServicePage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of ServiceInstance
        
        :param dict payload: Payload response from the API
        
        :returns: ServiceInstance
        :rtype: ServiceInstance
        """
        return ServiceInstance(
            self._version,
            payload,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Notifications.V1.ServicePage>'


class ServiceContext(InstanceContext):

    def __init__(self, version, sid):
        """
        Initialize the ServiceContext
        
        :param Version version: Version that contains the resource
        :param sid: The sid
        
        :returns: ServiceContext
        :rtype: ServiceContext
        """
        super(ServiceContext, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'sid': sid,
        }
        self._uri = '/Services/{sid}'.format(**self._solution)
        
        # Dependents
        self._bindings = None
        self._notifications = None

    def delete(self):
        """
        Deletes the ServiceInstance
        
        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete('delete', self._uri)

    def fetch(self):
        """
        Fetch a ServiceInstance
        
        :returns: Fetched ServiceInstance
        :rtype: ServiceInstance
        """
        params = values.of({})
        
        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )
        
        return ServiceInstance(
            self._version,
            payload,
            sid=self._solution['sid'],
        )

    def update(self, friendly_name=values.unset, apn_credential_sid=values.unset,
               gcm_credential_sid=values.unset, messaging_service_sid=values.unset,
               facebook_messenger_page_id=values.unset,
               default_apn_notification_protocol_version=values.unset,
               default_gcm_notification_protocol_version=values.unset):
        """
        Update the ServiceInstance
        
        :param unicode friendly_name: The friendly_name
        :param unicode apn_credential_sid: The apn_credential_sid
        :param unicode gcm_credential_sid: The gcm_credential_sid
        :param unicode messaging_service_sid: The messaging_service_sid
        :param unicode facebook_messenger_page_id: The facebook_messenger_page_id
        :param unicode default_apn_notification_protocol_version: The default_apn_notification_protocol_version
        :param unicode default_gcm_notification_protocol_version: The default_gcm_notification_protocol_version
        
        :returns: Updated ServiceInstance
        :rtype: ServiceInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'ApnCredentialSid': apn_credential_sid,
            'GcmCredentialSid': gcm_credential_sid,
            'MessagingServiceSid': messaging_service_sid,
            'FacebookMessengerPageId': facebook_messenger_page_id,
            'DefaultApnNotificationProtocolVersion': default_apn_notification_protocol_version,
            'DefaultGcmNotificationProtocolVersion': default_gcm_notification_protocol_version,
        })
        
        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )
        
        return ServiceInstance(
            self._version,
            payload,
            sid=self._solution['sid'],
        )

    @property
    def bindings(self):
        """
        Access the bindings
        
        :returns: BindingList
        :rtype: BindingList
        """
        if self._bindings is None:
            self._bindings = BindingList(
                self._version,
                service_sid=self._solution['sid'],
            )
        return self._bindings

    @property
    def notifications(self):
        """
        Access the notifications
        
        :returns: NotificationList
        :rtype: NotificationList
        """
        if self._notifications is None:
            self._notifications = NotificationList(
                self._version,
                service_sid=self._solution['sid'],
            )
        return self._notifications

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Notifications.V1.ServiceContext {}>'.format(context)


class ServiceInstance(InstanceResource):

    def __init__(self, version, payload, sid=None):
        """
        Initialize the ServiceInstance
        
        :returns: ServiceInstance
        :rtype: ServiceInstance
        """
        super(ServiceInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'sid': payload['sid'],
            'account_sid': payload['account_sid'],
            'friendly_name': payload['friendly_name'],
            'date_created': deserialize.iso8601_datetime(payload['date_created']),
            'date_updated': deserialize.iso8601_datetime(payload['date_updated']),
            'apn_credential_sid': payload['apn_credential_sid'],
            'gcm_credential_sid': payload['gcm_credential_sid'],
            'messaging_service_sid': payload['messaging_service_sid'],
            'facebook_messenger_page_id': payload['facebook_messenger_page_id'],
            'default_apn_notification_protocol_version': payload['default_apn_notification_protocol_version'],
            'default_gcm_notification_protocol_version': payload['default_gcm_notification_protocol_version'],
            'url': payload['url'],
            'links': payload['links'],
        }
        
        # Context
        self._context = None
        self._solution = {
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context
        
        :returns: ServiceContext for this ServiceInstance
        :rtype: ServiceContext
        """
        if self._context is None:
            self._context = ServiceContext(
                self._version,
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def sid(self):
        """
        :returns: The sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def friendly_name(self):
        """
        :returns: The friendly_name
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def date_created(self):
        """
        :returns: The date_created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date_updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def apn_credential_sid(self):
        """
        :returns: The apn_credential_sid
        :rtype: unicode
        """
        return self._properties['apn_credential_sid']

    @property
    def gcm_credential_sid(self):
        """
        :returns: The gcm_credential_sid
        :rtype: unicode
        """
        return self._properties['gcm_credential_sid']

    @property
    def messaging_service_sid(self):
        """
        :returns: The messaging_service_sid
        :rtype: unicode
        """
        return self._properties['messaging_service_sid']

    @property
    def facebook_messenger_page_id(self):
        """
        :returns: The facebook_messenger_page_id
        :rtype: unicode
        """
        return self._properties['facebook_messenger_page_id']

    @property
    def default_apn_notification_protocol_version(self):
        """
        :returns: The default_apn_notification_protocol_version
        :rtype: unicode
        """
        return self._properties['default_apn_notification_protocol_version']

    @property
    def default_gcm_notification_protocol_version(self):
        """
        :returns: The default_gcm_notification_protocol_version
        :rtype: unicode
        """
        return self._properties['default_gcm_notification_protocol_version']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def links(self):
        """
        :returns: The links
        :rtype: unicode
        """
        return self._properties['links']

    def delete(self):
        """
        Deletes the ServiceInstance
        
        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def fetch(self):
        """
        Fetch a ServiceInstance
        
        :returns: Fetched ServiceInstance
        :rtype: ServiceInstance
        """
        return self._proxy.fetch()

    def update(self, friendly_name=values.unset, apn_credential_sid=values.unset,
               gcm_credential_sid=values.unset, messaging_service_sid=values.unset,
               facebook_messenger_page_id=values.unset,
               default_apn_notification_protocol_version=values.unset,
               default_gcm_notification_protocol_version=values.unset):
        """
        Update the ServiceInstance
        
        :param unicode friendly_name: The friendly_name
        :param unicode apn_credential_sid: The apn_credential_sid
        :param unicode gcm_credential_sid: The gcm_credential_sid
        :param unicode messaging_service_sid: The messaging_service_sid
        :param unicode facebook_messenger_page_id: The facebook_messenger_page_id
        :param unicode default_apn_notification_protocol_version: The default_apn_notification_protocol_version
        :param unicode default_gcm_notification_protocol_version: The default_gcm_notification_protocol_version
        
        :returns: Updated ServiceInstance
        :rtype: ServiceInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
            apn_credential_sid=apn_credential_sid,
            gcm_credential_sid=gcm_credential_sid,
            messaging_service_sid=messaging_service_sid,
            facebook_messenger_page_id=facebook_messenger_page_id,
            default_apn_notification_protocol_version=default_apn_notification_protocol_version,
            default_gcm_notification_protocol_version=default_gcm_notification_protocol_version,
        )

    @property
    def bindings(self):
        """
        Access the bindings
        
        :returns: bindings
        :rtype: bindings
        """
        return self._proxy.bindings

    @property
    def notifications(self):
        """
        Access the notifications
        
        :returns: notifications
        :rtype: notifications
        """
        return self._proxy.notifications

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Notifications.V1.ServiceInstance {}>'.format(context)
