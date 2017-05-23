from __future__ import absolute_import

import sys
import os
import re
import json

import squareconnect
from squareconnect.api_client import ApiClient


class CardNonceApi(object):

    def __init__(self):
        self.api_client = ApiClient()

    def create_nonce(self, client_id, pan):
        #all_params = ['client_id', 'pan']
        params = locals()
        # verify the required parameter 'authorization' is set
        if ('client_id' not in params) or (params['client_id'] is None):
            raise ValueError("Missing the required parameter `client_id` when calling `create_card_nonce`")
        # verify the required parameter 'body' is set
        if ('pan' not in params) or (params['pan'] is None):
            raise ValueError("Missing the required parameter `pan` when calling `create_card_nonce`")

        resource_path = '/v2/card-nonce'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}
        form_params = []
        local_var_files = {}

        body_params = CreateCardNonceRequest(params['client_id'], params['pan'])

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        header_params['Origin'] = 'https://connect.squareup.com'
        header_params['X-Js-Id'] = "something"
        # Authentication setting
        auth_settings = []
        response = self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        
        deserialized_data = json.loads(response.data)
        return deserialized_data['card_nonce']

class CreateCardNonceRequest(object):

    def __init__(self, client_id, pan):
        self._client_id = client_id
        self._card_data = CardData(pan)
        self._session_id = "kdf0c1c90f2476bb9926adc4d28a6e8"
        self.swagger_types = {
            'client_id': 'str',
            'card_data': 'CardData',
            'session_id': 'str'
        }

        self.attribute_map = {
            'client_id': 'client_id',
            'card_data': 'card_data',
            'session_id': 'session_id'
        }

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id

    @property
    def card_data(self):
        return self._card_data

    @card_data.setter
    def card_data(self, card_data):
        self._card_data = card_data

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

class CardData(object):

    def __init__(self, pan):
        self._number = pan
        self._cvv = '112'
        self._exp_month = 12
        self._exp_year = 2024
        self._billing_postal_code = '94111'

        self.swagger_types = {
            'number': 'str',
            'cvv': 'str',
            'exp_month': 'int',
            'exp_year': 'int',
            'billing_postal_code': 'str'
        }

        self.attribute_map = {
            'number': 'number',
            'cvv': 'cvv',
            'exp_month': 'exp_month',
            'exp_year': 'exp_year',
            'billing_postal_code': 'billing_postal_code'
        }

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    @property
    def cvv(self):
        """
        Gets the cvv of this Card.

        :return: The cvv of this Card.
        :rtype: str
        """
        return self._cvv

    @cvv.setter
    def cvv(self, cvv):
        """
        Sets the cvv of this Card.

        :param cvv: The cvv of this Card.
        :type: str
        """
        self._cvv = cvv

    @property
    def exp_month(self):
        return self._exp_month

    @exp_month.setter
    def exp_month(self, exp_month):
        self._exp_month = exp_month

    @property
    def exp_year(self):
        return self._exp_year

    @exp_year.setter
    def exp_year(self, exp_year):
        self._exp_year = exp_year

    @property
    def billing_postal_code(self):
        return self._billing_postal_code

    @billing_postal_code.setter
    def billing_postal_code(self, billing_postal_code):
        self._billing_postal_code = billing_postal_code

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other