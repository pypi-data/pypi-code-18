"""
Each test function here covers a part of the specification.
They are run when the server returns a request.
If they fail, the client gets feedback.

About the test functions:
Please provide
- A short description of what is tested
- Links to the specification, where this is specified.

These test functions all relate to the "links" attribute of the search response.
- https://github.com/schul-cloud/resources-api-v1/tree/master/schemas/search-response#search-reponse-1

"""
from pytest import mark


@mark.skip(reason="TODO")
def test_self_link():
    """The self link is has the same offset and may have a reduced limit.
    """


@mark.skip(reason="TODO")
def test_limit_may_be_reduced():
    """If the limit is higher than the maximum limit the server has internally, the server sets the limit to the maximum available limit.
    """


@mark.skip(reason="TODO")
def test_count():
    """count is the actual number of objects retrieved.
    
    The count must be equal to the number of objects in the list.
    """


@mark.skip(reason="TODO")
def test_offset():
    """offset is the start index in the list of objects.
    
    The offset must be the same as requested.
    """


@mark.skip(reason="TODO")
def test_limit():
    """limit is the requested number of objects.

    
    """


@mark.skip(reason="TODO")
def test_the_end_is_reached():
    """If the end of the resource list is reached, count may be less than limit.
    
    This implies that there is no next link and the last link is self.
    """


@mark.skip(reason="TODO")
def test_no_resources_given():
    """If there are no resources, first, last, prev and next MUST be null.
    """


@mark.skip(reason="TODO")
def test_last_page_is_reached():
    """If the last page is reached, next MUST be null.
    
    This is tested by requesting the next page and getting no resources back.
    """


@mark.skip(reason="TODO")
def test_last_implies_next():
    """If last is given, next must be given.
    """


@mark.skip(reason="TODO")
def test_first_implies_prev():
    """If first is given, prev must be given.
    """


@mark.skip(reason="TODO")
def test_do_not_skip_objects():
    """The prev and next links MUST not skip objects.
    
    This can only be inferred by the limit and offset.
    """


@mark.skip(reason="TODO")
def test_retrieve_object_with_self_link():
    """If the object has a self link, it can be retrieved.
    
    This must be tested in parallel to reduce the waiting time.
    """


@mark.skip(reason="TODO")
def test_links_are_absolute():
    """All links are absolute links using the host header field.
    """


@mark.skip(reason="TODO")
def test_request_too_far():
    """Requesting beyond the last link yields no objects.
    """
