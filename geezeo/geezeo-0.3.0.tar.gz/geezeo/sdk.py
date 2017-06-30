# -*- coding: utf-8 -*-

"""
God object that controls API communication.
"""

import json, jwt, datetime, time
import os.path

import logging
import requests
import threading
from . import util
from . import aggregation


class SDK(object):

    """
    Consumer for the Geezeo API.

    The use of this package starts with an :class:`SDK` instance, which is
    created with the authentication information required by Geezeo's web API.

    The constructor can raise an :class:`UnauthorizedError` if ``api_key`` is
    incorrect, or a :class:`DoesNotExistError` if the ``user_id`` doesn't
    correspond to an actual user.

    All methods can raise :class:`ServerError` if an error occurred on the
    server, or :class:`NetworkError` if something goes wrong while attempting
    to communicate with the server.

    .. attribute:: api_key

        Authentication key for the partner institution using this SDK. If
        ``api_key`` is invalid, the constructor will raise an
        :class:`UnauthorizedError`.

    .. attribute:: user

        :class:`User` on whose behalf the SDK is being used. Note that the
        :class:`SDK` object is constructed with the string ``user_id``,
        and this attribute will be populated with the corresponding
        :class:`User` during construction.

    .. attribute:: url

        URL for the partner institution's web site. This will be the root of
        URLs for all requests made to the API.

    .. attribute:: sso_partner_id
        SSO Partner ID. If provided, the SDK will use JWT authentication
        instead of API key

    .. attribute:: jwt_ttl

        TTL to JWT tokens in seconds, default is 1 hour
    """

    def __init__(self, api_key, user_id, url, sso_partner_id = None, jwt_ttl=3600):
        self.api_key = api_key
        self.url = url
        self.session = requests.Session()
        self.sso_partner_id = sso_partner_id
        self.jwt_ttl = jwt_ttl
        self.user_id = user_id

        # This will raise UnauthorizedError if not authorized,
        # NotFoundError if the user does not exist,
        # NetworkError if the url is invalid.
        if self.use_jwt():
            logging.debug("Using JWT for Geezeo SDK Authentication")
        else:
            logging.debug("Using API for Geezeo SDK Authentication")
            self.user = self.get_user(user_id) # Not valid with JWT currently.

    def to_jwt(self):
        domain = self.url.split("//")[1]
        token = self.generate_jwt(self.sso_partner_id, self.user_id, domain, self.api_key, self.jwt_ttl)
        return token

    def use_jwt(self):
        return self.sso_partner_id

    @staticmethod
    def generate_jwt(sso_partner_id, user_id, url, api_key, ttl = 3600):
        if not sso_partner_id:
            raise util.GeezeoError("sso_partner_id required to generate a jwt token")
        if not user_id:
            raise util.GeezeoError("partner_customer_id required to generate a jwt token")
        if not url:
            raise util.GeezeoError("domain required to generate a jwt token")
        if not api_key:
            raise util.GeezeoError("secret required to generate a jwt token")
        if not ttl:
            raise util.GeezeoError("ttl required to generate a jwt token")

        issued = datetime.datetime.now()
        expires = issued + datetime.timedelta(0, ttl)

        payload = {
            'iss': sso_partner_id,
            'aud': url,
            'sub': user_id,
            'iat': time.mktime(issued.timetuple()),
            'exp': time.mktime(expires.timetuple())
        }
        token = jwt.encode(payload, api_key, algorithm='HS256')
        return token

    def request(self, method, path, **kwargs):
        """
        Make a request of the API.

        Additional arguments in ``kwargs`` will be passed to an underlying
        :func:`requests.request` call.

        .. _Geezeo: http://developers.geezeo.com

        :param str method: ``'GET'``, ``'POST'``, etc.
        :param str path: portion of the URL that follows :attr:`self.url
            <url>`. This should match the HTTP path in the `Geezeo`_ docs,
             e.g. ``'/api/v2/ping'``. Note that GET parameters should
            be managed with the ``params`` argument instead.
        :return: dictionary parsed from the JSON returned by the endpoint.
        """

        # s/get/GET/
        method = method.upper()

        # If the path starts with a slash, it is interpreted as a path from
        # root (consequence of using an os.path function to join components).
        if path.startswith('/'):
            path = path[1:]
        url = os.path.join(self.url, path)


        try:
            logging.debug('calling {0} on {1}'.format(method, url))

            if self.use_jwt():
                request = requests.Request(method, url, **kwargs)
                request.headers['Authorization'] = "Bearer " + self.to_jwt().decode("UTF-8")
            else:
                # Requests use HTTP basic auth, with the api_key as the username and
                # no password.
                auth = (self.api_key, '')
                request = requests.Request(method, url, auth=auth, **kwargs)

            content_type = 'application/json'
            if 'ce_fis' in url or 'classify' in url: # If using aggregation change content type to encoded form
                content_type = 'application/x-www-form-urlencoded'
            request.headers['Content-Type'] = content_type
            prepared_request = request.prepare()
            response = self.session.send(prepared_request)
        except requests.exceptions.RequestException as e:
            # The requests.request function raised an exception, indicating
            # that we didn't communicate successfully with the server.
            logging.debug('requests err : {0}'.format(type(e)), e)
            raise util.NetworkError(e)
        else:
            logging.debug('response code {0} body {1}'.format(response.status_code, response.text))
            # We got a response, but not necessarily a successful one.
            if response.status_code in [200, 201]:
                return response.json()
            if response.status_code == 204:
                return None
            elif response.status_code == 401:
                raise util.UnauthorizedError(response)
            elif response.status_code == 404:
                raise util.DoesNotExistError(response)
            elif response.status_code == 405:
                msg = 'invalid method for {0}: {1}'.format(path, method)
                raise ValueError(msg)
            elif response.status_code == 500:
                raise util.ServerError(response)
            else:
                logging.debug("UNHANDLED HTTP STATUS {0}".format(response.status_code))
                raise util.ServerError("Unhandled status : {0}".format(response.status_code))

    def ping(self):
        """
        Raise :class:`UnauthorizedError` if the SDK was not initialized
        correctly.
        """

        self.request('GET', '/api/v2/ping')

    def get_user(self, user_id = None):
        """
        Fetch the User with the user_id provided.

        :param string user_id: unique identifier, corresponds to
            :attr:`User.id`
        :raises DoesNotExistError: if no user with ID ``user_id`` exists.
        :return: the :class:`User` in question
        """
        if user_id is None:
            user_id = self.user_id

        body = self.request('GET', '/api/v2/users/{0}'.format(user_id))
        return util.User(body['users'][0])

    def pending_account_ids(self):
        """
        Generate IDs for pending accounts, which must be destroyed!
        """

        url = '/api/v2/users/{0}/pending_accounts'.format(self.user_id)
        data = self.request('GET', url)
        for fi in data['pending_accounts']:
            for id in fi['account_ids']:
                yield id

    def clear_pending_accounts(self):
        """
        Delete all of the user's pending accounts.

        This function retrieves a list of the account IDs for all of the
        user's pending accounts. It then spawns a thread for each one, which
        uses the API to delete that account. The function does not return
        until all threads have finished running.
        """

        # Given a pending account ID, make a request to delete it.
        def delete_account(id):
            url_template = '/api/v2/users/{0}/pending_accounts/{1}'
            self.request('DELETE', url_template.format(self.user_id, id))

        # Spawn a thread to delete each pending account.
        delete_threads = []
        for id in self.pending_account_ids():
            thread = threading.Thread(target=delete_account, args=(id,))
            delete_threads.append(thread)
            thread.start()

        # Wait for all pending accounts to be deleted.
        for thread in delete_threads:
            thread.join()

    def search_institutions(self, search_string, scope=None, page=1):
        """
        Search the set of institutions aggregated by the aggregation provider.

        .. note::

            If the search string is sufficiently vague, the results will be
            truncated. Since the API backing this function is paginated, the
            truncation will be to three pages of results.

        :param str search_string: keywords to search for
        :param str scope: if present, must be ``'name'`` or ``'url'``.
            determines how the institution needs to match ``search_string``.
        :param int page: (optional) page of results to retrieve. Get the
            first page by default.
        :return: :class:`PagedResults` whose :attr:`~PagedResults.data`
            is a list of :class:`AuthPrompt` objects for institutions
            matching the ``search_string``.
        """

        assert isinstance(page, int), 'page must be an integer'
        assert page > 0, 'page must be positive'
        params = {
            'q': search_string,
            'page': page,
        }

        if scope is not None:
            assert scope in ('name', 'url'), "Scope must be 'name' or 'url'"
            params['scope'] = scope

        data = self.request('GET', '/api/v2/ce_fis/search', params=params)
        prompts = [aggregation.AuthPrompt(item) for item in data['ce_fis']]
        current_page = data['meta']['current_page']
        last_page = data['meta']['total_pages']
        return util.PagedResults(prompts, current_page, last_page)

    def get_all_institutions(self, page=1):
        """
        Return a page from the set of all institutions.

        :param int page: (optional) page of results to retrieve. Get the
            first page by default.
        :return: :class:`PagedResults` whose :attr:`~PagedResults.data` is a
            list of :class:`AuthPrompt` objects.
        """

        assert isinstance(page, int), 'page must be an integer'
        assert page > 0, 'page must be positive'
        params = {
            'page': page
        }

        data = self.request('GET', '/api/v2/ce_fis', params=params)
        prompts = [aggregation.AuthPrompt(item) for item in data['ce_fis']]
        current_page = data['meta']['current_page']
        last_page = data['meta']['total_pages']
        return util.PagedResults(prompts, current_page, last_page)

    def get_institution(self, id):
        """
        Return a single institution.

        :param int id: id of fi.
        :return: :class:`PagedResults` whose :attr:`~PagedResults.data` is a
            list of :class:`AuthPrompt` objects.
        """

        assert isinstance(id, int), 'id must be an integer'
        assert id > 0, 'id must be positive'

        data = self.request('GET', '/api/v2/ce_fis/{0}'.format(id))
        if len(data['ce_fis']) == 0:
            raise util.DoesNotExistError
        prompts = [aggregation.AuthPrompt(item) for item in data['ce_fis']]
        return util.PagedResults(prompts, 1, 1)

    def get_accounts(self):
        """
        Return a list of accounts for a user

        :param int id: id of fi.
        :return: :class:`dict` whose schema is defined here https://developers.geezeo.com/#get-accounts
        """

        data = self.request('GET', '/api/v2/users/{0}/accounts'.format(self.user_id))
        if data.get('accounts', None) is None:
            raise util.DoesNotExistError
        return data['accounts']

    def get_aggregated_accounts(self):
        """
        Return a list of accounts for a user filtered for only aggregated

        :param int id: id of fi.
        :return: :class:`dict` whose schema is defined here https://developers.geezeo.com/#get-accounts
        """

        accounts = self.get_accounts()
        aggregated_accounts = [a for a in accounts if a['aggregation_type'] != 'partner']
        return aggregated_accounts

    def get_transactions(self):
        """
        Return a list of most recent transactions

        :return: :class:`dict` whose schema is defined here https://developers.geezeo.com/?shell#get-user-transactions
        """
        transactions = self.request("GET", "/api/v2/users/{0}/transactions".format(self.user_id))
        return transactions

    def get_networth(self):
        """
        Return a list of networth accounts

        :return: :class:`dict` whose schema is defined here https://developers.geezeo.com/#get-networth
        """
        networth_accounts = self.request("GET", "/api/v2/users/{0}/networth".format(self.user_id))
        return networth_accounts

    def create_network_account(self, account_type, balance, name):
        """
        Create a new worth account

        :return: :class:`dict` response
        """
        self.validate_networth_account(account_type, balance, name)

        payload = {
            'networth_account': {
                'account_type': account_type,
                'balance': balance,
                'name': name
            }
        }

        networth_account = self.request("POST", "/api/v2/users/{0}/networth/accounts".format(self.user_id), data=json.dumps(payload))
        return networth_account

    def update_network_account(self, networth_account_id, account_type, balance, name):
        """
        Create a new worth account

        :return: :class:`dict` response
        """
        if not networth_account_id: raise util.GeezeoError("networth_account_id is required")
        self.validate_networth_account(account_type, balance, name)

        payload = {
            'networth_account': {
                'account_type': account_type,
                'balance': balance,
                'name': name
            }
        }

        networth_account = self.request("PUT", "/api/v2/users/{0}/networth/accounts/{1}".format(self.user_id, networth_account_id), data=json.dumps(payload))
        return networth_account

    def validate_networth_account(self, account_type, balance, name):
        if account_type not in ['debt', 'asset']: raise util.GeezeoError("account_type is required")
        if not balance: raise util.GeezeoError("balance is required")
        if not name: raise util.GeezeoError("name is required")

    def update_transaction(self, transaction_id, nickname, tags, repeat_rule ='do_not_repeat', rules_accounts ='all_accounts'):
        """
        Updates a transaction

        :param int transaction_id: id of fi.
        :param str nickname: the nickname the user wants to apply, echo back nickname if not changing.
        :param arr tags: The categories being applied to this transaction in the form [{name:'name', value:5}] where all category values summed together must equal the balance of the transaction
        :param str repeat_rule: string that must be one of the following values ['do_not_repeat', 'repeat_future_dates', 'repeat_all_dates']
        :param str rules_accounts: If creating a rule, an optional account filter that must be one of the following values ['all_accounts', 'current_account'].
        :return: :class:`dict` whose schema is defined here https://developers.geezeo.com/#get-accounts
        """
        if not transaction_id: raise util.GeezeoError("id is required")
        if not nickname: raise util.GeezeoError("nickname is required")
        if not tags: raise util.GeezeoError("tags are required")
        if repeat_rule not in ['do_not_repeat', 'repeat_future_dates', 'repeat_all_dates']:
            raise util.GeezeoError("repeat rule not valid")
        if rules_accounts not in ['all_accounts', 'current_account']:
            raise util.GeezeoError("rules account not valid")

        if len(tags) > 1:
            def map_tag(tag): return {'name': tag.name, 'value': tag.value}
            mapped_tags = [map_tag(tag) for tag in tags]
            payload = {
                'transaction': {
                    'nickname': nickname,
                },
                'tagging': {
                    'type': 'split',
                    'split': mapped_tags,
                    'repeat': repeat_rule,
                    'account': rules_accounts
                }
            }
        else:
            payload = {
                'transaction': {
                    'nickname': nickname,
                },
                'tagging': {
                    'type': 'none',
                    'regular': [tags[0]["name"]]
                }
            }

        try:
            self.request('PUT', '/api/v2/users/{0}/transactions/{1}'.format(self.user_id, transaction_id), data=json.dumps(payload))
        except:
            return False

        return True

    def update_account(self, account_id, name):
        if not account_id:
            raise util.GeezeoError("account_id is required")
        if not name:
            raise util.GeezeoError("name is required")
        payload = {
            'account': {
                'name': name
            }
        }

        try:
            self.request("PUT", '/api/v2/users/{0}/accounts/{1}'.format(self.user_id, account_id), data=json.dumps(payload))
        except:
            return False

        return True

    def get_partner_accounts(self):
        """
        Return a list of accounts for a user filtered for only partner

        :param int id: id of fi.
        :return: :class:`dict` whose schema is defined here https://developers.geezeo.com/#get-accounts
        """

        accounts = self.get_accounts()
        partner_accounts = [a for a in accounts if a['aggregation_type'] == 'partner']
        return partner_accounts

    def delete_account(self, account_id):
        """
        Delete an account for a user

        :param int id: id of account.
        :return: bool
        """
        try:
            data = self.request('DELETE', '/api/v2/users/{0}/accounts/{1}'.format(self.user_id, account_id))
        except:
            return False
        return True

    def start_harvest(self):
        """
        Start a harvest on the Geezeo platform

        :return: :class:`Dict` Harvest results defined https://developers.geezeo.com/#harvests

        """

        data = self.request('POST', '/api/v2/users/{0}/harvest'.format(self.user_id))
        return data

    def get_harvest_status(self):
        """
        Get the harvest status for a user

        :return: :class:`Dict` Harvest results defined https://developers.geezeo.com/#harvests

        """

        data = self.request('GET', '/api/v2/users/{0}/harvest'.format(self.user_id))
        return data

    def is_harvesting(self):
        harvest_status = self.get_harvest_status()
        return harvest_status['harvests'][0]['status'] != 'complete'

    def get_featured_institutions(self):
        """
        Return the list of featured institutions for the current partner.

        :return: list of :class:`AuthPrompt` objects for institutions featured
            by the current partner.
        """

        # This is not available in the current API. Return any old FIs.
        return self.get_all_institutions(page=1).data

    def authenticate(self, submit_key, parameters):
        """
        Send login information to the aggregation provider for authentication.

        :param str submit_key: the :attr:`submit_key <AuthPrompt.submit_key>`
            attribute of the prompt for which to submit auth details
        :param dict parameters: dictionary (or dictionary-like object) mapping
            the IDs in this form's :attr:`parameters <AuthPrompt.parameters>`
            attribute to the user's corsubmiting login information
        :raises MFARequiredError: if the institution requires multi-factor
            authentication
        :raises UnauthorizedError: if the authentication fails
        :return: the :class:`AggregatedInstitution` for which the user has
            authenticated
        """

        # self.clear_pending_accounts() # this actually kills an inflight mfa
        submit_data = aggregation.decode_submit_key(submit_key)

        # Construct and send the request.

        if submit_data['type'] == 'auth':
            method = 'POST'
            url = '/api/v2/users/{0}/ce_fis'.format(self.user_id)
            fields = {
                'id': submit_data['id'],
            }
            for key, value in parameters.items():
                fields['credentials[login_params][{0}]'.format(key)] = value

        elif submit_data['type'] == 'mfa':
            method = 'PUT'
            url = '/api/v2/users/{0}/ce_fis/{1}'.format(self.user_id,
                                                        submit_data['id'])
            fields = {
                'harvest_id': submit_data['harvest_id'],
                'login_id': submit_data['login_id'],
                'session_key': submit_data['session_key'],
            }
            for key, value in parameters.items():
                fields['mfa_responses[{0}]'.format(key)] = value

        response = self.request(method, url, data=fields)

        # Determine what kind of information we got back, based on the JSON
        # data from the server.

        # Success, accompanied by a list of accounts.
        if 'accounts' in response:
            accounts = []
            classifications = {}
            for item in response['accounts']:

                # Prepare the list of accounts for the AggregatedInstitution
                # return value.
                accounts.append(util.Account(item))

                # Track the account type and ext type of each account for
                # classification.
                id = item['id']
                try:
                    acct_type = item['cashedge_account_type']['acct_type']
                    ext_type = item['cashedge_account_type']['ext_type']
                    types = (acct_type, ext_type)
                except (KeyError, TypeError):
                    types = None
                classifications[id] = types

            self.classify_accounts(classifications)
            return aggregation.AggregatedInstitution(submit_data, accounts)

        # MFA challenge
        elif 'response' in response:
            message = response['response']['message']
            data = response['response']['data']
            if 'mfa_parameters' in data:
                raise aggregation.MFARequiredError(message, data, submit_data)
            elif data.get('code') == 'bad_credentials':
                raise util.UnauthorizedError(response)

    def update_authentication(self, submit_key, parameters):
        """
        :param str submit_key: :attr:`~AggregatedInstitution.submit_key` of an
            institution whose auth info will be updated
        :param dict parameters: dictionary mapping the :attr:`key
            <AuthParameter.key>` attributes from :attr:`parameters
            <AggregatedInstitution.parameters>` to the new values for each one
        :raises MFARequiredError: if the institution requires multi-factor
            auth to change parameters
        :raises TypeError: if the parameters provided don't match the prompt
        """

        self.clear_pending_accounts()
        submit_data = aggregation.decode_submit_key(submit_key)
        institution_id = submit_data['id']

        # The old CashEdge API, for reasons that surpass understanding,
        # requires an account ID to update the authentication for an
        # institution. To preserve the sanity of our semantics, we use
        # the institution ID to look up an account ID for any
        # corresponding account, then use that account ID.
        #
        # This is wildly inefficient; we are resting on two things:
        #   1. Our plan to make this implementation obsolete.
        #   2. Our standing disclaimer that this call will take a long time.

        account_id = None
        accounts_url = '/api/v2/users/{0}/accounts'.format(self.user_id)
        accounts_response = self.request('GET', accounts_url)

        # Iterate through all the user's accounts until we find one from the
        # institution whose auth info we wish to update.

        for account in accounts_response['accounts']:
            if str(account['fi']['id']) == institution_id:
                account_id = account['id']
                break

        if account_id is None:
            raise util.DoesNotExistError('No accounts usable for updating '
                                         'credentials.')

        url_template = '/api/v2/users/{0}/accounts/{1}/update_credentials'
        url = url_template.format(self.user_id, account_id)

        # Populate the form data from the new values provided.

        if submit_data['type'] == 'institution':
            fields = {}
            for key, value in parameters:
                fields['credentials[login_params][{0}]'.format(key)] = value
        else:
            fields = {
                'harvest_id': submit_data['harvest_id'],
                'login_id': submit_data['login_id'],
                'session_key': submit_data['session_key'],
            }
            for key, value in parameters:
                fields['mfa_responses[{0}]'.format(key)] = value

        response = self.request('PUT', url, data=fields)
        if 'response' in response:
            message = response['response']
            data = response['data']
            raise aggregation.MFARequiredError(message, data, submit_data)

    def classify_accounts(self, classifications):
        """
        Update the account types for some set of accounts.

        :param dict classifications: Dictionary mapping string account IDs to
            either an ``(account_type, ext_type)`` pair or ``None``. If the
            value is ``None``, the account will be dropped from aggregation.
        """

        fields = {}
        for account_id, types in classifications.items():
            key = 'accounts[{0}][type_code]'.format(account_id)
            if types is None:
                value = 'ignore'
            else:
                account_type, ext_type = types
                value = '{0},{1}'.format(account_type, ext_type)
            fields[key] = value
        url = '/api/v2/users/{0}/accounts/classify'.format(self.user_id)
        response = self.request('PUT', url, data=fields)
        assert 'accounts' in response, 'Unexpected classification response.'
