"""
This file contains the fixtures used in the tests in the same folder.

"""
from pytest import fixture


@fixture
def query():
    """These are some query parameters passed over via the command line
    
    If not enough parameters are specified, a set of own paramaters is taken.
    They can be specified by the command line parameter --query.
    """


@fixture
def validateRequest():
    """Return a function to request results from the search engine.
    
    The results are validated.
    If it happens that the search engine does not provide a valid response, 
    the response is printed and an AssertionError is raised.
    """


@fixture
def max_depth():
    """Return a number of requests to perform at maximum.
    
    This limits the number of requests which are executed
    to get all search results.
    The can be specified by the command line parameter --max-depth.
    """
