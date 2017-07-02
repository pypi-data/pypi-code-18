from bottle import get, run, response
import json


@get("/<path:path>")
def get(path):
    """Return a search response."""
    response.set_header("Content-Type", "application/vnd.api+json")
    result = {
        "jsonapi": {
            "version": "1.0",
            "meta": {
                "name": "schul_cloud/schul_cloud_search_tests", 
                "source": 
                    "https://github.com/schul_cloud/schul_cloud_search_tests",
                "description":
                    "These are the tests for the search engines.",
            }
        }
    }
    return json.dumps(result)

if __name__ == "__main__":
    run(reload=True, port=8080)
