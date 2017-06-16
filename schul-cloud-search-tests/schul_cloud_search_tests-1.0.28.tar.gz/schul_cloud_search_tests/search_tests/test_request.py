"""
Each test function here covers a part of the specification.
All tests in here should be marked by 

    @mark.request

They are run on the clients request.
If they fail, the client gets feedback and the server does not get the request.

About the test functions:
Please provide
- A short description of what is tested
- Links to the specification, where this is specified.

"""
from pytest import mark
import pytest


@mark.request
def test_request_has_query(params):
    """Test that the query includes a "q".
    
    This is specified here:
    - https://github.com/schul-cloud/resources-api-v1/#search-api
    """
    assert params.get("q") is not None, (
        "Please pass a query string to with q=... to the request.")


@mark.request
@mark.parametrize("parameter", ["page[offset]", "page[limit]"])
def test_integer_parameters(params, parameter):
    """Test that page[offset] and page[limit] are positive integers.
    
    This is specified here:
    - https://github.com/schul-cloud/resources-api-v1/#search-api
    """
    value = params.get(parameter)
    if value is None:
        pytest.skip("parameter {} absent".format(parameter))
    assert value.isdigit(), (
        "The parameter {} must be a positive integer, not {}."
        .format(parameter, value))


@mark.request
@mark.skip(reason="TODO")
def test_json_api_content_type_is_accepted(search):
    """Make sure the Accept header allows application/vnd.api+json
    
    This is because the search api is jsonapi compatible.
    - https://github.com/schul-cloud/resources-api-v1/#search-api
    - http://jsonapi.org/format/#content-negotiation-clients
    
    Test for the existence of
    - application/vnd.api+json
    - application/*
    - */*
    without parameters.
    """


@mark.skip(reason="TODO")
def test_all_parameter_names_are_jsonapi_compatible():
    """If search engines add new parameters, they MUST be jsonapi compatible.
    
    See jsonapi
    - http://jsonapi.org/format/#query-parameters
    
    This includes:
    - parameter names
    - filter[ATTRIBUTE.XX.YY....]
    """
