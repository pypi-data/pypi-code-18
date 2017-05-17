import base64

import six

from .. import utils


class SecretApiMixin(object):
    @utils.minimum_version('1.25')
    def create_secret(self, name, data, labels=None):
        """
            Create a secret

            Args:
                name (string): Name of the secret
                data (bytes): Secret data to be stored
                labels (dict): A mapping of labels to assign to the secret

            Returns (dict): ID of the newly created secret
        """
        if not isinstance(data, bytes):
            data = data.encode('utf-8')

        data = base64.b64encode(data)
        if six.PY3:
            data = data.decode('ascii')
        body = {
            'Data': data,
            'Name': name,
            'Labels': labels
        }

        url = self._url('/secrets/create')
        return self._result(
            self._post_json(url, data=body), True
        )

    @utils.minimum_version('1.25')
    @utils.check_resource
    def inspect_secret(self, id):
        """
            Retrieve secret metadata

            Args:
                id (string): Full ID of the secret to remove

            Returns (dict): A dictionary of metadata

            Raises:
                :py:class:`docker.errors.NotFound`
                    if no secret with that ID exists
        """
        url = self._url('/secrets/{0}', id)
        return self._result(self._get(url), True)

    @utils.minimum_version('1.25')
    @utils.check_resource
    def remove_secret(self, id):
        """
            Remove a secret

            Args:
                id (string): Full ID of the secret to remove

            Returns (boolean): True if successful

            Raises:
                :py:class:`docker.errors.NotFound`
                    if no secret with that ID exists
        """
        url = self._url('/secrets/{0}', id)
        res = self._delete(url)
        self._raise_for_status(res)
        return True

    @utils.minimum_version('1.25')
    def secrets(self, filters=None):
        """
            List secrets

            Args:
                filters (dict): A map of filters to process on the secrets
                list. Available filters: ``names``

            Returns (list): A list of secrets
        """
        url = self._url('/secrets')
        params = {}
        if filters:
            params['filters'] = utils.convert_filters(filters)
        return self._result(self._get(url, params=params), True)
