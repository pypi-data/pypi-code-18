# -*- coding: utf-8 -*-
"""
:copyright: (c) 2015 - 2017 Stichting Koppeltaal
:license: AGPL, see `LICENSE.md` for more details.
"""

import urllib
import zope.interface

from koppeltaal.fhir import bundle, resource
from koppeltaal import (
    interfaces,
    logger,
    models,
    transport,
    utils)

DEFAULT_COUNT = 100


@zope.interface.implementer(interfaces.IIntegration)
class Integration(object):

    def __init__(
            self,
            name='Generic python application',
            url='https://example.com/fhir/Koppeltaal'):
        self.name = name
        self.url = url

    def transaction_hook(self, commit_function, message):
        return commit_function(message)

    def model_id(self, model):
        # You should in your implementation extend this class and
        # re-implement this method so that model_id() of a given model
        # always return the exact same id. This is NOT done here in
        # this simplistic default implementation.
        return id(model)

    def fhir_link(self, model, resource_type):
        return '{}/{}/{}'.format(
            self.url, resource_type, self.model_id(model))


@zope.interface.implementer(interfaces.IUpdate)
class Update(object):

    def __init__(self, message, resources, ack_function):
        self.message = message
        self.resources = resources
        self.data = message.data
        self.patient = message.patient
        self._ack_function = ack_function

    def __enter__(self):
        self.acked = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and exc_val is None and exc_tb is None:
            if self.acked is False:
                self.success()
        else:
            # There was an exception. We put back the message to new
            # since we assume we can be solved after.
            self.ack('New')
        if self.acked is not None:
            self._ack_function(self.message)

    def ack(self, status, exception=None):
        self.acked = True
        if self.message.status is None:
            self.message.status = models.Status()
        self.message.status.status = status
        self.message.status.exception = exception
        self.message.status.last_changed = utils.now()

    def success(self):
        self.ack('Success')

    def fail(self, exception="FAILED"):
        self.ack('Failed', unicode(exception))

    def postpone(self):
        self.acked = None


@zope.interface.implementer(interfaces.IConnector)
class Connector(object):
    _create_transport = transport.Transport

    def __init__(self, credentials, integration):
        self._credentials = credentials
        self.transport = self._create_transport(
            self._credentials.url,
            self._credentials.username,
            self._credentials.password)
        self.domain = self._credentials.domain
        self.integration = integration

    def _fetch_bundle(self, url, params=None):
        next_url = url
        next_params = params
        packaging = bundle.Bundle(self.domain, self.integration)
        while next_url:
            response = self.transport.query(next_url, next_params)
            packaging.add_payload(response.json)
            next_url = utils.json2links(response.json).get('next')
            next_params = None  # Parameters are already in the next link.
        return packaging

    def metadata(self):
        return self.transport.query(interfaces.METADATA_URL).json

    def activities(self, archived=False):
        params = {'code': 'ActivityDefinition'}
        if archived:
            params['includearchived'] = 'yes'
        return self._fetch_bundle(
            interfaces.ACTIVITY_DEFINITION_URL, params).unpack()

    def activity(self, identifier, archived=False):
        for activity in self.activities(archived=archived):
            if activity.identifier == identifier:
                return activity
        return None

    def send_activity(self, activity):
        packaging = resource.Resource(self.domain, self.integration)
        packaging.add_model(activity)
        payload = packaging.get_payload()
        if activity.fhir_link is not None:
            response = self.transport.update(activity.fhir_link, payload)
        else:
            response = self.transport.create(interfaces.OTHER_URL, payload)
        if response.location is None:
            raise interfaces.InvalidResponse(response)
        activity.fhir_link = response.location
        return activity

    def launch(self, careplan, user=None, activity_identifier=None):
        activity = None
        for candidate in careplan.activities:
            if (activity_identifier is None or
                    candidate.identifier == activity_identifier):
                activity = candidate
                break
        if activity is None:
            raise interfaces.KoppeltaalError('No activity found')
        if user is None:
            user = careplan.patient
        application_id = None
        if activity.definition is not None:
            activity_definition = self.activity(activity.definition)
            assert interfaces.IReferredFHIRResource.providedBy(
                activity_definition.application)
            application_id = activity_definition.application.display
        return self.launch_from_parameters(
            application_id,
            careplan.patient.fhir_link,
            user.fhir_link,
            activity.identifier)

    def launch_from_parameters(
            self,
            application_id,
            patient_link,
            user_link,
            activity_identifier):
        assert application_id is not None, 'Invalid activity'
        assert patient_link is not None, 'Invalid patient'
        assert user_link is not None, 'Invalid user'
        params = {
            'client_id': application_id,
            'patient': patient_link,
            'user': user_link,
            'resource': activity_identifier}
        return self.transport.query_redirect(
            interfaces.OAUTH_LAUNCH_URL, params).location

    def authorize_from_parameters(
            self,
            application_id,
            launch_id,
            redirect_uri):
        assert application_id is not None, 'Invalid activity'
        return '{}?{}'.format(
            self.transport.absolute_url(interfaces.OAUTH_AUTHORIZE_URL),
            urllib.urlencode(
                (('client_id', application_id),
                 ('redirect_uri', redirect_uri),
                 ('response_type', 'code'),
                 ('scope', 'patient/*.read launch:{}'.format(launch_id)))))

    def token_from_parameters(self, code, redirect_url):
        params = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_url}
        # Note how for this specific request a different set of credentials
        # ought to be used.
        # See https://www.koppeltaal.nl/
        #    wiki/Technical_Design_Document_Koppeltaal_1.1.1
        #    #6._Game_retrieves_an_Access_token
        username = self.integration.client_id
        password = self.integration.client_secret
        assert username is not None, 'client id missing'
        assert password is not None, 'client secret missing'
        return self.transport.query(
            interfaces.OAUTH_TOKEN_URL,
            params=params,
            username=username,
            password=password).json

    def updates(self, expected_events=None):

        def send_back(message):
            packaging = resource.Resource(self.domain, self.integration)
            packaging.add_model(message)
            self.transport.update(message.fhir_link, packaging.get_payload())

        def send_back_on_transaction(message):
            return self.integration.transaction_hook(send_back, message)

        p = {'_query': 'MessageHeader.GetNextNewAndClaim'}
        while True:
            try:
                bundle = self._fetch_bundle(interfaces.MESSAGE_HEADER_URL, p)
                message = bundle.unpack_message_header()
            except interfaces.InvalidBundle as error:
                logger.error(
                    'Bundle error while reading message: {}'.format(error))
                continue
            except interfaces.InvalidResponse as error:
                logger.error(
                    'Transport error while reading mailbox: {}'.format(error))
                break

            if message is None:
                # We are out of messages
                break

            update = Update(message, bundle.unpack, send_back_on_transaction)
            errors = bundle.errors()

            if errors:
                logger.error('Error while reading message: {}'.format(errors))
                with update:
                    update.fail(u', '.join([u"Resource '{}': {}".format(
                        e.fhir_link, e.error) for e in errors]))
            elif (expected_events is not None
                  and message.event not in expected_events):
                logger.warn('Event "{}" not expected'.format(message.event))
                with update:
                    update.fail('Event not expected')
            elif message.source.endpoint == self.integration.url:
                logger.info(
                    'Event "{}" originated from our endpoint '
                    '"{}"'.format(message.event, self.integration.url))
                with update:
                    # We are the sender ourselves. Ack those messages.
                    update.success()
            else:
                yield update

    def search(
            self, message_id=None, event=None, status=None, patient=None):
        params = {}
        if message_id:
            params['_id'] = message_id
        else:
            params['_summary'] = 'true'
            params['_count'] = DEFAULT_COUNT
        if event:
            params['event'] = event
        if status:
            params['ProcessingStatus'] = status
        if patient:
            params['Patient'] = patient.fhir_link
        return self._fetch_bundle(
            interfaces.MESSAGE_HEADER_URL,
            params).unpack()

    def send(self, event, data, patient=None):
        identifier = utils.messageid()
        source = models.MessageHeaderSource(
            name=unicode(self.integration.name),
            endpoint=unicode(self.integration.url),
            software=unicode(interfaces.SOFTWARE),
            version=unicode(interfaces.VERSION))
        message = models.MessageHeader(
            timestamp=utils.now(),
            event=event,
            identifier=identifier,
            data=data,
            source=source,
            patient=patient)
        send_bundle = bundle.Bundle(self.domain, self.integration)
        send_bundle.add_model(message)
        response_bundle = bundle.Bundle(self.domain, self.integration)
        response_bundle.add_payload(
            self.transport.create(
                interfaces.MAILBOX_URL,
                send_bundle.get_payload()).json)
        response = response_bundle.unpack_message_header()
        if (response is None or
                response.response is None or
                response.response.identifier != identifier or
                response.response.code != "ok"):
            raise interfaces.InvalidResponse(response)
        return response.data
