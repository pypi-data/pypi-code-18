import base64
import logging
import json
import requests
from .compat import string_types


log = logging.getLogger(__name__)


class SessionError(Exception):
    """Raised when a REST call gets a non-2XX HTTP error code."""


class Session(object):

    ENDPOINT_URL = 'https://www.clevertim.com/api'

    ENDPOINT_FACTORY = {}

    def __init__(self, api_key, endpoint_url=None, enable_caching=True):
        assert api_key, "Empty API key"
        self.api_key = api_key
        endpoint_url = endpoint_url or self.ENDPOINT_URL
        self.endpoint_url = endpoint_url.rstrip('/')
        self.enable_caching = enable_caching
        # used to cache GET requests
        self.session_cache = {}
        self.instance_cache = {}

    @property
    def url(self):
        return self.endpoint_url

    @classmethod
    def register_endpoint(cls, endpoint_cls, accepted_types=None):
        accepted_types = accepted_types or (endpoint_cls,)
        cls.register_endpoint_factory(endpoint_cls, endpoint_cls, accepted_types=accepted_types)

    @classmethod
    def register_endpoint_factory(cls, endpoint, endpoint_factory, accepted_types=None):
        if not isinstance(endpoint, string_types):
            endpoint = endpoint.__name__
        cls.ENDPOINT_FACTORY[endpoint] = (endpoint_factory, accepted_types)

    @classmethod
    def deregister_endpoint(cls, endpoint_cls):
        if not isinstance(endpoint_cls, string_types):
            endpoint_cls = endpoint_cls.__name__
        del cls.ENDPOINT_FACTORY[endpoint_cls]

    @classmethod
    def enpoint_accepted_types(cls, endpoint_name):
        return cls.ENDPOINT_FACTORY[endpoint_name][1]

    @classmethod
    def is_registered_endpoint(cls, endpoint_name_or_cls):
        if isinstance(endpoint_name_or_cls, string_types):
            return endpoint_name_or_cls in cls.ENDPOINT_FACTORY
        ret = getattr(endpoint_name_or_cls, '__name__')
        if ret:
            return ret in cls.ENDPOINT_FACTORY
        return False

    @staticmethod
    def build_url(url, endpoint, resource_id=None):
        if not endpoint.startswith('/'):
            url += '/'
        url += endpoint.rstrip('/')
        if resource_id:
            url += '/' + str(resource_id)
        return url

    def _get_url(self, endpoint, resource_id=None):
        return self.build_url(self.endpoint_url, endpoint, resource_id=resource_id)

    def _get_cache_key(self, endpoint, resource_id):
        return '%s%s' % (endpoint, resource_id or '')

    def _get_cached_value(self, endpoint, resource_id):
        if self.enable_caching:
            cache_key = self._get_cache_key(endpoint, resource_id)
            ret = self.session_cache.get(cache_key)
            if ret:
                return ret

    def _update_cache(self, endpoint, resource_id, result):
        if self.enable_caching:
            for res in result:
                cache_key = self._get_cache_key(endpoint, res['id'])
                self.session_cache[cache_key] = res

    def _clear_cache(self, endpoint, resource_id):
        if self.enable_caching:
            cache_key = self._get_cache_key(endpoint, resource_id)
            try:
                del self.session_cache[cache_key]
            except KeyError:
                pass

    def make_request(self, endpoint, resource_id=None, method='GET', payload=None, load_all=False, reload=False):
        assert endpoint, "Empty endpoint"

        auth_key = self.api_key + ':X'
        auth_token = base64.standard_b64encode(auth_key.encode('ascii'))
        headers = {
            'Authorization': 'Basic %s' % (auth_token,),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        url = self._get_url(endpoint, resource_id=None if load_all else resource_id)

        if method == "GET":
            if not reload:
                val = self._get_cached_value(endpoint, resource_id)
                if val is not None:
                    log.debug("cache hit on GET %s", url)
                    return val
            log.debug("GET %s", url)
            r = requests.get(url, headers=headers)
        elif method == "POST":
            log.debug("POST %s %s", url, payload)
            r = requests.post(url, headers=headers, data=json.dumps(payload, separators=(',', ':')))
        elif method == "PUT":
            log.debug("PUT %s %s", url, payload)
            r = requests.put(url, headers=headers, data=json.dumps(payload, separators=(',', ':')))
        elif method == "DELETE":
            log.debug("DELETE %s", url)
            r = requests.delete(url, headers=headers)
        else:
            assert False, "Unknown method: '%s'" % (method,)

        status_code = r.status_code
        response = r.text

        if status_code != 200:
            raise SessionError("HTTP %s - %s" % (status_code, response))

        log.debug("Response %s %s", r.status_code, response)
        result = response and json.loads(response) or None

        if result is not None:
            # update or clear the cache
            if method != 'DELETE':
                result = result['content']

                self._update_cache(endpoint, resource_id, result)

                if method != 'GET':
                    result = result[0]
                elif resource_id is not None:
                    result = [res for res in result if res.get('id') == resource_id]
                    if not result:
                        raise SessionError("Not found.")
                    result = result[0]
            else:
                self._clear_cache(endpoint, resource_id)

        return result

    def get(self, endpoint, key, lazy_load=False):
        if not isinstance(endpoint, string_types):
            endpoint = endpoint.__name__
        cache_key = '%s%s' % (endpoint, key)
        instance = self.instance_cache.get(cache_key)
        if instance is None:
            cls = self.ENDPOINT_FACTORY[endpoint][0]
            instance = cls(self, key=key, lazy_load=lazy_load)
            self.instance_cache[cache_key] = instance
        return instance
