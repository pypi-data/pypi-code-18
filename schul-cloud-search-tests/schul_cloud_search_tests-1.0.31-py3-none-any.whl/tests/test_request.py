from schul_cloud_resources_api_v1.schema import get_schemas
from pytest import mark
from schul_cloud_search_tests.tests.assertions import assertIsError, ERROR_CLIENT_REQUEST
from pprint import pprint


@mark.parametrize("param", ["page[offset]", "page[limit]"])
@mark.parametrize("value", ["", "asd", "-1"])
def test_parameter_must_be_positive_integer(search_engine, param, value):
    """
    According to
    - https://github.com/schul-cloud/resources-api-v1#search-api
    - http://jsonapi.org/format/#fetching-pagination
    page[offset] and page[limit] must be positive integers.
    
    This is an invalid request, according to
    - https://github.com/schul-cloud/schul_cloud_search_tests#specification
    the return code must be ERROR_CLIENT_REQUEST.
    """
    result = search_engine.request(params={param:value, "q":"test"})
    assert result.status_code == ERROR_CLIENT_REQUEST
    assertIsError(result.json(), ERROR_CLIENT_REQUEST)
    
    
def test_q_is_a_required_query(search_engine):
    """
    According to the Search API https://github.com/schul-cloud/resources-api-v1#search-api
    q is required
    """
    result = search_engine.request(params={})
    assert result.status_code == ERROR_CLIENT_REQUEST
    data = result.json()
    assertIsError(data, ERROR_CLIENT_REQUEST)
    errors = [error for error in data["errors"]
             if error["meta"].get("test_function") == "test_request_has_query"]
    assert errors, "There should be such an error function"
    meta = errors[0]["meta"]
    assert meta["source"] == search_engine.proxy_url + "code/search_tests/test_request.py"
    from schul_cloud_search_tests.search_tests.test_request import test_request_has_query
    assert meta["line"] == test_request_has_query.__code__.co_firstlineno



