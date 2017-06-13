from bottle import Bottle
from schul_cloud_resources_server_tests.tests.fixtures import StoppableWSGIRefServerAdapter

app = Bottle()





def main(host="0.0.0.0", port=8080):
    """Start the server."""
    server = StoppableWSGIRefServerAdapter()
    app.get("/stop", callback=server.shutdown)
    app.run(host=host, port=port, debug=True, reloader=True, server=server)

__all__ = ["main", "app"]

if __name__ == "__main__":
    main()
