import json
import time

import requests
from concurrent import futures
from requests.exceptions import ConnectionError

from ppg_common.errors import (
    ButterCupHTTPErrors, ButterCupHTTPException, BlossomHTTPError,
    BlossomHTTPErrors, BubblesHttpError, BubblesHttpErrors,
    PpgHttpErrors, PpgHTTPError
)


def retry(func):
    def wrapper(self, *args, **kwargs):
        for i in range(3):
            try:
                return func(self, *args, **kwargs)
            except ConnectionError:
                time.sleep(2 ** (i + 1))
        raise PpgHTTPError(PpgHttpErrors.WENT_WRONG)

    return wrapper


def handle_response(func):
    def wrapper(self, *args, **kwargs):
        if kwargs.get('headers') is None:
            kwargs['headers'] = {}
        kwargs['headers'].update(self.base_headers)
        response = func(self, *args, **kwargs)
        body = None
        if len(response.content):
            body = response.json()
        if 400 <= response.status_code < 500 and body and body.get(
                'message') and body.get('code'):
            if 100 <= body.get('code') < 200:
                raise ButterCupHTTPException(
                    ButterCupHTTPErrors.error_map[body.get('code')])
            if 200 <= body.get('code') < 300:
                raise BlossomHTTPError(
                    BlossomHTTPErrors.error_map[body.get('code')])
            if 300 <= body.get('code') < 400:
                raise BubblesHttpError(
                    BubblesHttpErrors.error_map[body.get('code')])
        # if self.base_session is not None:
        self.base_headers.update({'x-session': self.base_session})
        # else:
        #     self.base_headers.pop('x-session')
        return body

    return wrapper


class BaseClient(object):
    version = '/v1'

    def __init__(self, host, port, ssl=False, session=None):
        if ssl:
            self.base_url = "https://{}:{}".format(host, port)
        else:
            self.base_url = "http://{}:{}".format(host, port)

        self.base_headers = {
            'Accept': 'application/json', 'Content-Type': 'application/json'
        }

        self.base_session = session
        if session is not None:
            self.base_headers.update({'x-session': session})

        self.tp = futures.ThreadPoolExecutor(max_workers=8)

    def create_url(self, path):
        return "{}{}".format(self.base_url, path)

    def with_session(self, session_id):
        self.base_headers.update({'x-session': session_id})
        return self

    def change_session(self, session_id):
        self.base_headers.update({'x-session': session_id})

    def get_status(self):
        url = self.create_url(BaseClient.version + '/status')
        return requests.get(url, verify=False)

    @retry
    @handle_response
    def get(self, path, query=None, headers=None):
        url = self.create_url(path)
        future = self.tp.submit(requests.get, url, headers=headers,params=query)
        return future.result()

    @retry
    @handle_response
    def post(self, path, body=None, query=None, headers=None):
        if body is None:
            body = {}
        url = self.create_url(path)
        future = self.tp.submit(
            requests.post, url, headers=headers, data=json.dumps(body),params=query
        )
        return future.result()

    @retry
    @handle_response
    def put(self, path, body=None, query=None, headers=None):
        if body is None:
            body = {}
        url = self.create_url(path)
        future = self.tp.submit(
            requests.put, url, headers=headers, data=json.dumps(body),params=query
        )
        return future.result()

    @retry
    @handle_response
    def patch(self, path, body=None, query=None, headers=None):
        if body is None:
            body = {}
        url = self.create_url(path)
        future = self.tp.submit(
            requests.patch, url, headers=headers, data=json.dumps(body),params=query
        )
        return future.result()

    @retry
    @handle_response
    def delete(self, path, query=None, headers=None):
        url = self.create_url(path)
        future = self.tp.submit(requests.delete, url, headers=headers,params=query)
        return future.result()

