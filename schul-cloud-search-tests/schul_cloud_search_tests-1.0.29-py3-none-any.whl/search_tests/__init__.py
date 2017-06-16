"""
Run the tests.

"""
import pytest
import os
import threading
import io
import traceback
import inspect

HERE = os.path.dirname(__file__)
_local = threading.local()


def get_documentation(tb):
    """Return the documentation from the first test functions found."""
    while tb:
        for func in tb.tb_frame.f_globals.values():
            if inspect.isfunction(func) and \
                    func.__name__.startswith("test_") and \
                    func.__code__ == tb.tb_frame.f_code:
                return func.__doc__
        tb = tb.tb_next


def run_request_tests(request_url):
    """Run the tests with the request."""
    return _run_tests_and_collect_errors(request_url, ["-m" "request", HERE])


def run_response_tests(request_url, response):
    """Run the tests with the request and response."""
    _local.response = response
    try:
        return _run_tests_and_collect_errors(request_url, ["-m" "not request", HERE])
    finally:
        del _local.response


def get_response():
    """Return the currently working response."""
    return _local.response


def get_request_url():
    """Return the url of the test server endpoint with the query."""
    return _local.request_url


def add_failing_test(ty, err, tb):
    """Add a failing test to the tests of this request."""
    file = io.StringIO()
    traceback.print_exception(ty, err, tb, file=file)
    tb_string = file.getvalue()
    _local.failing_tests.append({
          "status": 500, 
          "title": "Internal Server Error",
          "detail": ty.__name__ + ": " + str(err),
          "meta": {
            "traceback" : tb_string,
            "documentation": get_documentation(tb),
            "error-class": ty.__module__ + "." + ty.__name__
          }
        })


def _run_tests_and_collect_errors(request_url, args):
    """Run the tests and collect the errors in these tests."""
    _local.failing_tests = []
    _local.request_url = request_url
    try:
        pytest.main(args)
        return _local.failing_tests
    finally:
        del _local.failing_tests
        del _local.request_url

