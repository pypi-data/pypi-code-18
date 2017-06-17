from bottle import Bottle, request, response
import sys
import os
import requests
from schul_cloud_resources_server_tests.tests.fixtures import StoppableWSGIRefServerAdapter
if "" in sys.path:
    sys.path.append(".")
from schul_cloud_search_tests.search_tests import run_request_tests, run_response_tests

ENDPOINT_STOP = "/stop"
REDIRECT_TO = "http://localhost:8080"


def pytest_errors(errors, server_url, answer=None):
    """Return the formatted pytest errors, jsonapi compatible."""
    response.status = 409
    result = {
      "errors":[
        {
          "status": 409,
          "title": "Conflict",
          "detail": "The request or response contained some errors.",
          "meta": {
            "url": server_url,
            "response": answer
          }
        }
      ] + errors,
      "jsonapi": {
        "version": "1.0",
        "meta": {
          "name": "schul_cloud/schul_cloud_search_tests", 
          "source": 
            "https://github.com/schul-cloud/schul_cloud_search_tests",
          "description":
            "These are the tests for the search engines."
        }
      }
    }
    return result


def test_response(target_url):
    """Test the request and the response to the search engine."""
    print("query string:", request.query_string)
    server_url = target_url + "?" + request.query_string
    errors = run_request_tests(server_url)
    if errors:
        return pytest_errors(errors, server_url)
    answer = requests.get(server_url)
    errors = run_response_tests(server_url, answer)
    try:
        result = answer.json()
    except ():
        result = None
    if errors:
        return pytest_errors(errors, server_url, result)
    assert result is not None, "The tests take care that there is a result."
    return result


def get_code():
    """Return a directory listing or a static file."""
    


def get_app(endpoint="/", target_url="http://localhost:8080"):
    """Return a bottle app that tests the request and the response."""
    app = Bottle()
    app.get(endpoint, callback=lambda: test_response(target_url))
    return app


def run(app, host="0.0.0.0", port=8081):
    """Run a stoppable bottle app."""
    server = StoppableWSGIRefServerAdapter(host=host, port=port)
    app.get(ENDPOINT_STOP, callback=lambda: server.shutdown(blocking=False))
    app.run(debug=True, server=server)
    

def main(host="0.0.0.0", port=8081, endpoint="/", target_url="http://localhost:8080"):
    """Start the server."""
    app = get_app(endpoint=endpoint, target_url=target_url)
    run(app, host=host, port=port)


__all__ = ["main", "app"]

if __name__ == "__main__":
    main()
