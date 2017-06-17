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

