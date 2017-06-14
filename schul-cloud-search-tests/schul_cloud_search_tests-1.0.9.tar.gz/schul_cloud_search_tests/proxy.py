from bottle import Bottle, request
import sys
from schul_cloud_resources_server_tests.tests.fixtures import StoppableWSGIRefServerAdapter

ENDPOINT_STOP = "/stop"
REDIRECT_TO = "http://localhost:8080"

app = Bottle()

hook = app.hook




def main(host="0.0.0.0", port=8081, endpoint="/"):
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
    app.get(ENDPOINT_STOP, callback=lambda: server.shutdown(blocking=False))
    app.run(debug=True, server=server)

__all__ = ["main", "app"]

if __name__ == "__main__":
    main()
