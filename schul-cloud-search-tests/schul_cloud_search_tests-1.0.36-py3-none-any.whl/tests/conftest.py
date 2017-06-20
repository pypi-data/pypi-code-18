"""
This file contains the test configuration like fixtures.
"""
from pytest import fixture
from schul_cloud_resources_server_tests.tests.fixtures import ParallelBottleServer
from bottle import Bottle, request
import sys
import os
import requests
from urllib.parse import urlencode
import copy


HERE = os.path.dirname(__file__)
MODULE_ROOT = os.path.join(HERE, "..", "..")
try:
    import schul_cloud_search_tests
except ImportError:
    sys.path.append(MODULE_ROOT)
from schul_cloud_search_tests.proxy import get_app


class Requester(object):
    """Shortcut to request a hosted resource."""
    
    def __init__(self, url):
        """Create a requester."""
        self._url = url
    
    def request(self):
        """Request the resource."""
        return requests.get(self._url)


def ending_with_slash(url):
    """Return the url with a slash in the end."""
    if not url.endswith("/"):
        url = url + "/"
    return url


def params_to_key(params):
    """Return a tuple key for the parameters."""
    key = list(params.items())
    key.sort()
    return tuple(key)

class SearchEngine(object):
    """The search engine adapter.
    
    This includes:
    - the running search tests server
    - a bottle server returning the registeres responses
    """
    
    _default_response = {
      "jsonapi": {
        "version": "1.0",
        "meta" : {
          "name": "Example Server",
          "source": "https://github.com/schul-cloud/resources-api-v1",
          "description": "This is just an eampel server for the search API."
        }
      },
      "links": {
        "self": {
          "href": None,
          "meta": {
            "count": 0,
            "offset": 0,
            "limit": 0
          }
        },
        "first": None,
        "last": None,
        "prev": None,
        "next": None
      },
      "data": []
    }

    def __init__(self):
        """Create a search engine object."""
        self._queries = {}
        self._app = Bottle()
        self._app.get("/", callback=self._serve_request)
        self._reset_servers()
    
    def start(self):
        """Start the search engine tests and the search engine mock."""
        assert not self.is_started()
        self._server = ParallelBottleServer(self._app)
        self._search_app = get_app(target_url=self.search_engine_url)
        self._search_server = ParallelBottleServer(self._search_app)
        
    @property
    def search_engine_url(self):
        """Return the URL of the mocked search engine."""
        assert self.is_started()
        return ending_with_slash(self._server.url)

    @property
    def proxy_url(self):
        """Return the url of the search engine tests proxy."""
        assert self.is_started()
        return ending_with_slash(self._search_server.url)
        
    def stop(self):
        """Stop the search engine tests and the mock server."""
        assert self.is_started()
        self._server.shutdown()
        self._search_server.shutdown()
        self._reset_servers()

    def _reset_servers(self):
        """Create the starting condition"""
        self._server = None
        self._search_server = None
        self._search_app = None

    def is_started(self):
        """Return whether the server is started."""
        return self._server is not None
        
    def host(self, response, params={}):
        """Host the response given by the query."""
        key = params_to_key(params)
        assert key not in self._queries
        self._queries[key] = response
        return self._new_requester(params)
    
    def clear(self):
        """Remove all hosted responses."""
        self._queries = {}
        self._last_response = None

    def _serve_request(self):
        """Serve a request to the search engine bottle server."""
        default = self.get_default_response(request.query_string)
        response = self._queries.get(params_to_key(request.query), default)
        self._last_response = response
        return response

    def request(self, params={}):
        """Request a search with parameters."""
        return self._new_requester(params).request()
        
    def _new_requester(self, params):
        """Return a new Requester object from the parameters."""
        request_url = self.proxy_url + "?" + urlencode(params)
        return Requester(request_url)
        
    def get_default_response(self, query_string):
        """Return the default response to a query."""
        result = copy.deepcopy(self._default_response)
        url = self.search_engine_url + "?" + query_string
        result["links"]["self"]["href"] = url
        return result
        
    @property
    def last_response(self):
        """Return the last reponse of the search engine to a request.
        
        If there was no request, None is returned.
        """
        return self._last_response


@fixture(scope="session")
def search_engine_session():
    """Return the server to store resources."""
    server = SearchEngine()
    server.start()
    yield server
    server.stop()


@fixture
def search_engine(search_engine_session):
    """Return a fresh server object with no resources."""
    search_engine_session.clear()
    yield search_engine_session
    search_engine_session.clear()


@fixture
def code_url(search_engine):
    """Return the url of the code enpoint."""
    return search_engine.proxy_url + "code"