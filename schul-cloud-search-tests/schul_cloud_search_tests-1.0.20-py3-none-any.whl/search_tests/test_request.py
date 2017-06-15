from pytest import mark


@mark.request
def test_request_has_query(request):
    """Test that the query includes a "q"."""
    assert "q" in request.query





