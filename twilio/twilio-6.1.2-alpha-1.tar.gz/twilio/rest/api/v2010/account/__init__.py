# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.api.v2010.account.address import AddressList
from twilio.rest.api.v2010.account.application import ApplicationList
from twilio.rest.api.v2010.account.authorized_connect_app import AuthorizedConnectAppList
from twilio.rest.api.v2010.account.available_phone_number import AvailablePhoneNumberCountryList
from twilio.rest.api.v2010.account.call import CallList
from twilio.rest.api.v2010.account.conference import ConferenceList
from twilio.rest.api.v2010.account.connect_app import ConnectAppList
from twilio.rest.api.v2010.account.incoming_phone_number import IncomingPhoneNumberList
from twilio.rest.api.v2010.account.key import KeyList
from twilio.rest.api.v2010.account.message import MessageList
from twilio.rest.api.v2010.account.new_key import NewKeyList
from twilio.rest.api.v2010.account.new_signing_key import NewSigningKeyList
from twilio.rest.api.v2010.account.notification import NotificationList
from twilio.rest.api.v2010.account.outgoing_caller_id import OutgoingCallerIdList
from twilio.rest.api.v2010.account.queue import QueueList
from twilio.rest.api.v2010.account.recording import RecordingList
from twilio.rest.api.v2010.account.short_code import ShortCodeList
from twilio.rest.api.v2010.account.signing_key import SigningKeyList
from twilio.rest.api.v2010.account.sip import SipList
from twilio.rest.api.v2010.account.token import TokenList
from twilio.rest.api.v2010.account.transcription import TranscriptionList
from twilio.rest.api.v2010.account.usage import UsageList
from twilio.rest.api.v2010.account.validation_request import ValidationRequestList


class AccountList(ListResource):

    def __init__(self, version):
        """
        Initialize the AccountList

        :param Version version: Version that contains the resource

        :returns: twilio.rest.api.v2010.account.AccountList
        :rtype: twilio.rest.api.v2010.account.AccountList
        """
        super(AccountList, self).__init__(version)

        # Path Solution
        self._solution = {}
        self._uri = '/Accounts.json'.format(**self._solution)

    def create(self, friendly_name=values.unset):
        """
        Create a new AccountInstance

        :param unicode friendly_name: A human readable description of the account

        :returns: Newly created AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
        })

        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )

        return AccountInstance(
            self._version,
            payload,
        )

    def stream(self, friendly_name=values.unset, status=values.unset, limit=None,
               page_size=None):
        """
        Streams AccountInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode friendly_name: FriendlyName to filter on
        :param AccountInstance.Status status: Status to filter on
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.AccountInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            friendly_name=friendly_name,
            status=status,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, friendly_name=values.unset, status=values.unset, limit=None,
             page_size=None):
        """
        Lists AccountInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode friendly_name: FriendlyName to filter on
        :param AccountInstance.Status status: Status to filter on
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.AccountInstance]
        """
        return list(self.stream(
            friendly_name=friendly_name,
            status=status,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, friendly_name=values.unset, status=values.unset,
             page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of AccountInstance records from the API.
        Request is executed immediately

        :param unicode friendly_name: FriendlyName to filter on
        :param AccountInstance.Status status: Status to filter on
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountPage
        """
        params = values.of({
            'FriendlyName': friendly_name,
            'Status': status,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return AccountPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a AccountContext

        :param sid: Fetch by unique Account Sid

        :returns: twilio.rest.api.v2010.account.AccountContext
        :rtype: twilio.rest.api.v2010.account.AccountContext
        """
        return AccountContext(
            self._version,
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a AccountContext

        :param sid: Fetch by unique Account Sid

        :returns: twilio.rest.api.v2010.account.AccountContext
        :rtype: twilio.rest.api.v2010.account.AccountContext
        """
        return AccountContext(
            self._version,
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.AccountList>'


class AccountPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the AccountPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: twilio.rest.api.v2010.account.AccountPage
        :rtype: twilio.rest.api.v2010.account.AccountPage
        """
        super(AccountPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of AccountInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountInstance
        """
        return AccountInstance(
            self._version,
            payload,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.AccountPage>'


class AccountContext(InstanceContext):

    def __init__(self, version, sid):
        """
        Initialize the AccountContext

        :param Version version: Version that contains the resource
        :param sid: Fetch by unique Account Sid

        :returns: twilio.rest.api.v2010.account.AccountContext
        :rtype: twilio.rest.api.v2010.account.AccountContext
        """
        super(AccountContext, self).__init__(version)

        # Path Solution
        self._solution = {
            'sid': sid,
        }
        self._uri = '/Accounts/{sid}.json'.format(**self._solution)

        # Dependents
        self._addresses = None
        self._applications = None
        self._authorized_connect_apps = None
        self._available_phone_numbers = None
        self._calls = None
        self._conferences = None
        self._connect_apps = None
        self._incoming_phone_numbers = None
        self._keys = None
        self._messages = None
        self._new_keys = None
        self._new_signing_keys = None
        self._notifications = None
        self._outgoing_caller_ids = None
        self._queues = None
        self._recordings = None
        self._signing_keys = None
        self._sip = None
        self._short_codes = None
        self._tokens = None
        self._transcriptions = None
        self._usage = None
        self._validation_requests = None

    def fetch(self):
        """
        Fetch a AccountInstance

        :returns: Fetched AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountInstance
        """
        params = values.of({})

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return AccountInstance(
            self._version,
            payload,
            sid=self._solution['sid'],
        )

    def update(self, friendly_name=values.unset, status=values.unset):
        """
        Update the AccountInstance

        :param unicode friendly_name: FriendlyName to update
        :param AccountInstance.Status status: Status to update the Account with

        :returns: Updated AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'Status': status,
        })

        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )

        return AccountInstance(
            self._version,
            payload,
            sid=self._solution['sid'],
        )

    @property
    def addresses(self):
        """
        Access the addresses

        :returns: twilio.rest.api.v2010.account.address.AddressList
        :rtype: twilio.rest.api.v2010.account.address.AddressList
        """
        if self._addresses is None:
            self._addresses = AddressList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._addresses

    @property
    def applications(self):
        """
        Access the applications

        :returns: twilio.rest.api.v2010.account.application.ApplicationList
        :rtype: twilio.rest.api.v2010.account.application.ApplicationList
        """
        if self._applications is None:
            self._applications = ApplicationList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._applications

    @property
    def authorized_connect_apps(self):
        """
        Access the authorized_connect_apps

        :returns: twilio.rest.api.v2010.account.authorized_connect_app.AuthorizedConnectAppList
        :rtype: twilio.rest.api.v2010.account.authorized_connect_app.AuthorizedConnectAppList
        """
        if self._authorized_connect_apps is None:
            self._authorized_connect_apps = AuthorizedConnectAppList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._authorized_connect_apps

    @property
    def available_phone_numbers(self):
        """
        Access the available_phone_numbers

        :returns: twilio.rest.api.v2010.account.available_phone_number.AvailablePhoneNumberCountryList
        :rtype: twilio.rest.api.v2010.account.available_phone_number.AvailablePhoneNumberCountryList
        """
        if self._available_phone_numbers is None:
            self._available_phone_numbers = AvailablePhoneNumberCountryList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._available_phone_numbers

    @property
    def calls(self):
        """
        Access the calls

        :returns: twilio.rest.api.v2010.account.call.CallList
        :rtype: twilio.rest.api.v2010.account.call.CallList
        """
        if self._calls is None:
            self._calls = CallList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._calls

    @property
    def conferences(self):
        """
        Access the conferences

        :returns: twilio.rest.api.v2010.account.conference.ConferenceList
        :rtype: twilio.rest.api.v2010.account.conference.ConferenceList
        """
        if self._conferences is None:
            self._conferences = ConferenceList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._conferences

    @property
    def connect_apps(self):
        """
        Access the connect_apps

        :returns: twilio.rest.api.v2010.account.connect_app.ConnectAppList
        :rtype: twilio.rest.api.v2010.account.connect_app.ConnectAppList
        """
        if self._connect_apps is None:
            self._connect_apps = ConnectAppList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._connect_apps

    @property
    def incoming_phone_numbers(self):
        """
        Access the incoming_phone_numbers

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.IncomingPhoneNumberList
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.IncomingPhoneNumberList
        """
        if self._incoming_phone_numbers is None:
            self._incoming_phone_numbers = IncomingPhoneNumberList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._incoming_phone_numbers

    @property
    def keys(self):
        """
        Access the keys

        :returns: twilio.rest.api.v2010.account.key.KeyList
        :rtype: twilio.rest.api.v2010.account.key.KeyList
        """
        if self._keys is None:
            self._keys = KeyList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._keys

    @property
    def messages(self):
        """
        Access the messages

        :returns: twilio.rest.api.v2010.account.message.MessageList
        :rtype: twilio.rest.api.v2010.account.message.MessageList
        """
        if self._messages is None:
            self._messages = MessageList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._messages

    @property
    def new_keys(self):
        """
        Access the new_keys

        :returns: twilio.rest.api.v2010.account.new_key.NewKeyList
        :rtype: twilio.rest.api.v2010.account.new_key.NewKeyList
        """
        if self._new_keys is None:
            self._new_keys = NewKeyList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._new_keys

    @property
    def new_signing_keys(self):
        """
        Access the new_signing_keys

        :returns: twilio.rest.api.v2010.account.new_signing_key.NewSigningKeyList
        :rtype: twilio.rest.api.v2010.account.new_signing_key.NewSigningKeyList
        """
        if self._new_signing_keys is None:
            self._new_signing_keys = NewSigningKeyList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._new_signing_keys

    @property
    def notifications(self):
        """
        Access the notifications

        :returns: twilio.rest.api.v2010.account.notification.NotificationList
        :rtype: twilio.rest.api.v2010.account.notification.NotificationList
        """
        if self._notifications is None:
            self._notifications = NotificationList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._notifications

    @property
    def outgoing_caller_ids(self):
        """
        Access the outgoing_caller_ids

        :returns: twilio.rest.api.v2010.account.outgoing_caller_id.OutgoingCallerIdList
        :rtype: twilio.rest.api.v2010.account.outgoing_caller_id.OutgoingCallerIdList
        """
        if self._outgoing_caller_ids is None:
            self._outgoing_caller_ids = OutgoingCallerIdList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._outgoing_caller_ids

    @property
    def queues(self):
        """
        Access the queues

        :returns: twilio.rest.api.v2010.account.queue.QueueList
        :rtype: twilio.rest.api.v2010.account.queue.QueueList
        """
        if self._queues is None:
            self._queues = QueueList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._queues

    @property
    def recordings(self):
        """
        Access the recordings

        :returns: twilio.rest.api.v2010.account.recording.RecordingList
        :rtype: twilio.rest.api.v2010.account.recording.RecordingList
        """
        if self._recordings is None:
            self._recordings = RecordingList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._recordings

    @property
    def signing_keys(self):
        """
        Access the signing_keys

        :returns: twilio.rest.api.v2010.account.signing_key.SigningKeyList
        :rtype: twilio.rest.api.v2010.account.signing_key.SigningKeyList
        """
        if self._signing_keys is None:
            self._signing_keys = SigningKeyList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._signing_keys

    @property
    def sip(self):
        """
        Access the sip

        :returns: twilio.rest.api.v2010.account.sip.SipList
        :rtype: twilio.rest.api.v2010.account.sip.SipList
        """
        if self._sip is None:
            self._sip = SipList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._sip

    @property
    def short_codes(self):
        """
        Access the short_codes

        :returns: twilio.rest.api.v2010.account.short_code.ShortCodeList
        :rtype: twilio.rest.api.v2010.account.short_code.ShortCodeList
        """
        if self._short_codes is None:
            self._short_codes = ShortCodeList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._short_codes

    @property
    def tokens(self):
        """
        Access the tokens

        :returns: twilio.rest.api.v2010.account.token.TokenList
        :rtype: twilio.rest.api.v2010.account.token.TokenList
        """
        if self._tokens is None:
            self._tokens = TokenList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._tokens

    @property
    def transcriptions(self):
        """
        Access the transcriptions

        :returns: twilio.rest.api.v2010.account.transcription.TranscriptionList
        :rtype: twilio.rest.api.v2010.account.transcription.TranscriptionList
        """
        if self._transcriptions is None:
            self._transcriptions = TranscriptionList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._transcriptions

    @property
    def usage(self):
        """
        Access the usage

        :returns: twilio.rest.api.v2010.account.usage.UsageList
        :rtype: twilio.rest.api.v2010.account.usage.UsageList
        """
        if self._usage is None:
            self._usage = UsageList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._usage

    @property
    def validation_requests(self):
        """
        Access the validation_requests

        :returns: twilio.rest.api.v2010.account.validation_request.ValidationRequestList
        :rtype: twilio.rest.api.v2010.account.validation_request.ValidationRequestList
        """
        if self._validation_requests is None:
            self._validation_requests = ValidationRequestList(
                self._version,
                account_sid=self._solution['sid'],
            )
        return self._validation_requests

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.AccountContext {}>'.format(context)


class AccountInstance(InstanceResource):

    class Status(object):
        ACTIVE = "active"
        SUSPENDED = "suspended"
        CLOSED = "closed"

    class Type(object):
        TRIAL = "Trial"
        FULL = "Full"

    def __init__(self, version, payload, sid=None):
        """
        Initialize the AccountInstance

        :returns: twilio.rest.api.v2010.account.AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountInstance
        """
        super(AccountInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'auth_token': payload['auth_token'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'friendly_name': payload['friendly_name'],
            'owner_account_sid': payload['owner_account_sid'],
            'sid': payload['sid'],
            'status': payload['status'],
            'subresource_uris': payload['subresource_uris'],
            'type': payload['type'],
            'uri': payload['uri'],
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

        :returns: AccountContext for this AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountContext
        """
        if self._context is None:
            self._context = AccountContext(
                self._version,
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def auth_token(self):
        """
        :returns: The authorization token for this account
        :rtype: unicode
        """
        return self._properties['auth_token']

    @property
    def date_created(self):
        """
        :returns: The date this account was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date this account was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def friendly_name(self):
        """
        :returns: A human readable description of this account
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def owner_account_sid(self):
        """
        :returns: The unique 34 character id representing the parent of this account
        :rtype: unicode
        """
        return self._properties['owner_account_sid']

    @property
    def sid(self):
        """
        :returns: A 34 character string that uniquely identifies this resource.
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def status(self):
        """
        :returns: The status of this account
        :rtype: AccountInstance.Status
        """
        return self._properties['status']

    @property
    def subresource_uris(self):
        """
        :returns: Account Instance Subresources
        :rtype: unicode
        """
        return self._properties['subresource_uris']

    @property
    def type(self):
        """
        :returns: The type of this account
        :rtype: AccountInstance.Type
        """
        return self._properties['type']

    @property
    def uri(self):
        """
        :returns: The URI for this resource, relative to `https://api.twilio.com`
        :rtype: unicode
        """
        return self._properties['uri']

    def fetch(self):
        """
        Fetch a AccountInstance

        :returns: Fetched AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountInstance
        """
        return self._proxy.fetch()

    def update(self, friendly_name=values.unset, status=values.unset):
        """
        Update the AccountInstance

        :param unicode friendly_name: FriendlyName to update
        :param AccountInstance.Status status: Status to update the Account with

        :returns: Updated AccountInstance
        :rtype: twilio.rest.api.v2010.account.AccountInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
            status=status,
        )

    @property
    def addresses(self):
        """
        Access the addresses

        :returns: twilio.rest.api.v2010.account.address.AddressList
        :rtype: twilio.rest.api.v2010.account.address.AddressList
        """
        return self._proxy.addresses

    @property
    def applications(self):
        """
        Access the applications

        :returns: twilio.rest.api.v2010.account.application.ApplicationList
        :rtype: twilio.rest.api.v2010.account.application.ApplicationList
        """
        return self._proxy.applications

    @property
    def authorized_connect_apps(self):
        """
        Access the authorized_connect_apps

        :returns: twilio.rest.api.v2010.account.authorized_connect_app.AuthorizedConnectAppList
        :rtype: twilio.rest.api.v2010.account.authorized_connect_app.AuthorizedConnectAppList
        """
        return self._proxy.authorized_connect_apps

    @property
    def available_phone_numbers(self):
        """
        Access the available_phone_numbers

        :returns: twilio.rest.api.v2010.account.available_phone_number.AvailablePhoneNumberCountryList
        :rtype: twilio.rest.api.v2010.account.available_phone_number.AvailablePhoneNumberCountryList
        """
        return self._proxy.available_phone_numbers

    @property
    def calls(self):
        """
        Access the calls

        :returns: twilio.rest.api.v2010.account.call.CallList
        :rtype: twilio.rest.api.v2010.account.call.CallList
        """
        return self._proxy.calls

    @property
    def conferences(self):
        """
        Access the conferences

        :returns: twilio.rest.api.v2010.account.conference.ConferenceList
        :rtype: twilio.rest.api.v2010.account.conference.ConferenceList
        """
        return self._proxy.conferences

    @property
    def connect_apps(self):
        """
        Access the connect_apps

        :returns: twilio.rest.api.v2010.account.connect_app.ConnectAppList
        :rtype: twilio.rest.api.v2010.account.connect_app.ConnectAppList
        """
        return self._proxy.connect_apps

    @property
    def incoming_phone_numbers(self):
        """
        Access the incoming_phone_numbers

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.IncomingPhoneNumberList
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.IncomingPhoneNumberList
        """
        return self._proxy.incoming_phone_numbers

    @property
    def keys(self):
        """
        Access the keys

        :returns: twilio.rest.api.v2010.account.key.KeyList
        :rtype: twilio.rest.api.v2010.account.key.KeyList
        """
        return self._proxy.keys

    @property
    def messages(self):
        """
        Access the messages

        :returns: twilio.rest.api.v2010.account.message.MessageList
        :rtype: twilio.rest.api.v2010.account.message.MessageList
        """
        return self._proxy.messages

    @property
    def new_keys(self):
        """
        Access the new_keys

        :returns: twilio.rest.api.v2010.account.new_key.NewKeyList
        :rtype: twilio.rest.api.v2010.account.new_key.NewKeyList
        """
        return self._proxy.new_keys

    @property
    def new_signing_keys(self):
        """
        Access the new_signing_keys

        :returns: twilio.rest.api.v2010.account.new_signing_key.NewSigningKeyList
        :rtype: twilio.rest.api.v2010.account.new_signing_key.NewSigningKeyList
        """
        return self._proxy.new_signing_keys

    @property
    def notifications(self):
        """
        Access the notifications

        :returns: twilio.rest.api.v2010.account.notification.NotificationList
        :rtype: twilio.rest.api.v2010.account.notification.NotificationList
        """
        return self._proxy.notifications

    @property
    def outgoing_caller_ids(self):
        """
        Access the outgoing_caller_ids

        :returns: twilio.rest.api.v2010.account.outgoing_caller_id.OutgoingCallerIdList
        :rtype: twilio.rest.api.v2010.account.outgoing_caller_id.OutgoingCallerIdList
        """
        return self._proxy.outgoing_caller_ids

    @property
    def queues(self):
        """
        Access the queues

        :returns: twilio.rest.api.v2010.account.queue.QueueList
        :rtype: twilio.rest.api.v2010.account.queue.QueueList
        """
        return self._proxy.queues

    @property
    def recordings(self):
        """
        Access the recordings

        :returns: twilio.rest.api.v2010.account.recording.RecordingList
        :rtype: twilio.rest.api.v2010.account.recording.RecordingList
        """
        return self._proxy.recordings

    @property
    def signing_keys(self):
        """
        Access the signing_keys

        :returns: twilio.rest.api.v2010.account.signing_key.SigningKeyList
        :rtype: twilio.rest.api.v2010.account.signing_key.SigningKeyList
        """
        return self._proxy.signing_keys

    @property
    def sip(self):
        """
        Access the sip

        :returns: twilio.rest.api.v2010.account.sip.SipList
        :rtype: twilio.rest.api.v2010.account.sip.SipList
        """
        return self._proxy.sip

    @property
    def short_codes(self):
        """
        Access the short_codes

        :returns: twilio.rest.api.v2010.account.short_code.ShortCodeList
        :rtype: twilio.rest.api.v2010.account.short_code.ShortCodeList
        """
        return self._proxy.short_codes

    @property
    def tokens(self):
        """
        Access the tokens

        :returns: twilio.rest.api.v2010.account.token.TokenList
        :rtype: twilio.rest.api.v2010.account.token.TokenList
        """
        return self._proxy.tokens

    @property
    def transcriptions(self):
        """
        Access the transcriptions

        :returns: twilio.rest.api.v2010.account.transcription.TranscriptionList
        :rtype: twilio.rest.api.v2010.account.transcription.TranscriptionList
        """
        return self._proxy.transcriptions

    @property
    def usage(self):
        """
        Access the usage

        :returns: twilio.rest.api.v2010.account.usage.UsageList
        :rtype: twilio.rest.api.v2010.account.usage.UsageList
        """
        return self._proxy.usage

    @property
    def validation_requests(self):
        """
        Access the validation_requests

        :returns: twilio.rest.api.v2010.account.validation_request.ValidationRequestList
        :rtype: twilio.rest.api.v2010.account.validation_request.ValidationRequestList
        """
        return self._proxy.validation_requests

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.AccountInstance {}>'.format(context)
