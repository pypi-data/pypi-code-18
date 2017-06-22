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


def test_count_is_less_or_equal_to_the_limit(self_link):
    """The limit is the maximum number of objects returned.
    """
    assert self_link["meta"]["count"] <= self_link["meta"]["limit"]


def test_limit_may_be_reduced(self_link, limit):
    """If the limit is higher than the maximum limit the server has internally, the server sets the limit to the maximum available limit.
    """
    assert limit is None or self_link["meta"]["limit"] <= limit


def test_count(self_link, search_response):
    """count is the actual number of objects retrieved.
    
    The count must be equal to the number of objects in the list.
    """
    assert len(search_response["data"]) == self_link["meta"]["count"]


def test_offset(self_link, offset):
    """offset is the start index in the list of objects.
    
    The offset must be the same as requested.
    When a query is done without offset, the requested offset is zero.
    """
    assert self_link["meta"]["offset"] == offset


# TODO: put this into the specification to make it clear
def test_the_end_is_reached(self_link, links):
    """If the end of the resource list is reached, count may be less than limit.
    
    This implies that 
    - there is no next link and 
    - if there are resources, the last link is self 
    - if there are no resources in this request
      - the last link is pointing to a lesser offset or
      - the last link is null
    """
    if self_link["meta"]["count"] and \
            self_link["meta"]["count"] < self_link["meta"]["limit"]:
        assert links["next"] is None
        assert self_link["href"] == links["last"]
    elif self_link["href"] == links["last"]:
        assert links["next"] is None


def test_no_resources_given(search_response, links, offset):
    """If there are no resources, first, last, prev and next MUST be null.
    """
    if len(search_response["data"]) == 0:
        if offset == 0:
            assert links["last"] is None
            assert links["first"] is None
        assert links["prev"] is None
        assert links["next"] is None


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
