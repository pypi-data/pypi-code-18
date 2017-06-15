"""
Run the tests.

"""
import pytest
import os
import threading

HERE = os.path.dirname(__file__)


def run_request_tests():
    """Run the tests with the request."""
    pytest.main(["-m" "request", HERE])


_responses = threading.local()

def run_response_tests(response):
    """Run the tests with the request and response."""
    _responses.response = response
    try:
        pytest.main(["-m" "not request", HERE])
    finally:
        del _responses.response

def get_response():
    """Return the currently working response."""
    return _responses.response