"""
Run tests for the requests and responses.

If you mark your test with
@pytest.mark.request
your test is executed when the request arrives.

"""

from pytest import fixture
from schul_cloud_search_tests.search_tests import get_response

@fixture
def request():
    """The request to the server."""
    from bottle import request
    return request

@fixture
def response():
    """The response of the query."""
    return get_response()

