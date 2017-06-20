"""
Each test function here covers a part of the specification.
They are run when the server returns a request.
If they fail, the client gets feedback.

About the test functions:
Please provide
- A short description of what is tested
- Links to the specification, where this is specified.

"""
from pytest import mark
from schul_cloud_resources_api_v1.schema import get_schemas


@mark.skip(reason="TODO")
def test_response_schema(result):
    """If the request was successful, it must match the search-response schema.
    
    Schema:
    - https://github.com/schul-cloud/resources-api-v1/tree/master/schemas/search-response
    
    The response is successful of a status code 200 is returned.
    """


@mark.skip(reason="TODO")
def test_400_and_500_status_codes_have_the_jsonapi_design():
    """If the status code is 4XX, it contains a list of errors.

    Schema:
    - https://github.com/schul-cloud/resources-api-v1/tree/master/schemas/error
    """


@mark.skip(reason="TODO")
def test_the_content_type_is_from_the_jsonapi():
    """Make sure the returned content type is specified and expected.
    
    See here:
    - http://jsonapi.org/format/#content-negotiation-clients
    """
