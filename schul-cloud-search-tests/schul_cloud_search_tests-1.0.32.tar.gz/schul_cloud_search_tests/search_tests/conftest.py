"""
Run tests for the requests and responses.

If you mark your test with
@pytest.mark.request
your test is executed when the request arrives.

"""

from pytest import fixture, hookimpl
from schul_cloud_search_tests.search_tests import (
    get_response, add_failing_test, get_request_url
)
import pytest


try:
    pytest.skip()
except Exception as e:
    SKIP_ERROR = e.__class__


@fixture
def search():
    """The request to the server.
    
    The request from the client
    - http://bottlepy.org/docs/dev/api.html#bottle.BaseRequest
    """
    from bottle import request
    return request


@fixture
def result():
    """The response to the query.
    
    The response from the server.
    - http://docs.python-requests.org/en/master/api/#requests.Response
    """
    return get_response()


@fixture
def search_url():
    """The url of the server to request searches from."""
    return get_request_url()


@fixture
def params(search):
    """The query parameters.
    
    The search request parameters:
    - http://bottlepy.org/docs/dev/api.html#bottle.FormsDict
    
    You can use params.get("q") to get the "q" parameter.
    """
    return search.query


@hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    # From
    # - https://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-plugins
    # Also see 
    # - https://docs.pytest.org/en/latest/_modules/_pytest/vendored_packages/pluggy.html#_CallOutcome
    # for outcome
    
    outcome = yield
    # outcome.excinfo may be None or a (cls, val, tb) tuple
    if outcome.excinfo is not None and outcome.excinfo[0] not in (SKIP_ERROR,):
        add_failing_test(*outcome.excinfo)
    res = outcome.get_result()
