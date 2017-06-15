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


app = Bottle()

hook = app.hook

def test_response(target_url):
    run_request_tests()
    print("query string:", request.query_string)
    response = requests.get(target_url + "?" + request.query_string)
    run_response_tests(response)
    return response.body


def main(host="0.0.0.0", port=8081, endpoint="/", target_url="http://localhost:8080"):
    """Start the server."""
    server = StoppableWSGIRefServerAdapter(host=host, port=port)
    @hook('before_request')
    def strip_path():
        # from http://bottlepy.org/docs/dev/recipes.html#ignore-trailing-slashes
        path = request.environ['PATH_INFO']
        if path == ENDPOINT_STOP:
            return
        assert path.startswith(endpoint)
        path = path[len(endpoint):]
        if path[:1] != "/":
            path = "/" + path
        request.environ['PATH_INFO'] = path
    app.get(endpoint, callback=lambda: test_response(target_url))
    app.get(ENDPOINT_STOP, callback=lambda: server.shutdown(blocking=False))
    app.run(debug=True, server=server)

__all__ = ["main", "app"]

if __name__ == "__main__":
    main()
