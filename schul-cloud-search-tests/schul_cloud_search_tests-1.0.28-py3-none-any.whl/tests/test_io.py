from schul_cloud_resources_api_v1.schema import get_schemas
from pytest import mark
from schul_cloud_search_tests.tests.assertions import assertIsError, ERROR_CLIENT_REQUEST
from pprint import pprint




@mark.parametrize("response", get_schemas()["search-response"].get_valid_examples())
def test_valid_query_is_returned(search_engine, response):
    result = search_engine.host(response, {"q":"test"}).request()
    data = result.json()
    pprint(data)
    assert data == response


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
    
    
@mark.skip(reason="TODO")
def test_q_is_a_required_query():
    """
    According to the Search API https://github.com/schul-cloud/resources-api-v1#search-api
    q is required
    """
    

