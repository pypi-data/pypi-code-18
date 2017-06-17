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

    def _serve_request(self):
        """Serve a request to the search engine bottle server."""
        return self._queries.get(params_to_key(request.query))

    def request(self, params={}):
        """Request a search with parameters."""
        return self._new_requester(params).request()
        
    def _new_requester(self, params):
        """Return a new Requester object from the parameters."""
        request_url = self.proxy_url + "?" + urlencode(params)
        return Requester(request_url)


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
