from bottle import Bottle, request
import sys
import os
import requests
from schul_cloud_resources_server_tests.tests.fixtures import StoppableWSGIRefServerAdapter
if "" in sys.path:
    sys.path.append(".")
from schul_cloud_search_tests.search_tests import run_request_tests, run_response_tests

ENDPOINT_STOP = "/stop"
REDIRECT_TO = "http://localhost:8080"


def test_response(target_url):
    """Test the request and the response to the search engine."""
    run_request_tests()
    print("query string:", request.query_string)
    response = requests.get(target_url + "?" + request.query_string)
    run_response_tests(response)
    return response.body


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
