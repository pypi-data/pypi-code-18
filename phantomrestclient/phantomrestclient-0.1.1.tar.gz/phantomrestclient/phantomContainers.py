import os
import uuid
from basePhantom import _BasePhantom

class _PhantomContainers(_BasePhantom):
    """
    Wrapper around the Phantom REST calls for Containers
    """
    def __init__(self, host, username, password):
        _BasePhantom.__init__(self, host, username, password)
        self.endpoint_url = os.path.join(self.host, "container")

    def query(self, query=None):
        url = self.endpoint_url
        if query is not None:
            url += "?%s" % query

        return self.__make_rest_request__(url, "GET")

    def get_container(self, container_id):
        if container_id is None:
            raise ValueError("container_id is required")

        url = os.path.join(self.endpoint_url, str(container_id))
        return self.__make_rest_request__(url, "GET")

    def create(self, data):
        if "description" not in data or "label" not in data or "name" not in data:
            raise KeyError("required key missing")

        return self.__make_rest_request__(self.endpoint_url, "POST", data=data)

    def add_artifacts(self, container_id, artifacts, label="Test"):
        if container_id is None:
            raise ValueError("container_id is required")

        if artifacts is None:
            raise ValueError("artifacts is required")

        endpoint_url = os.path.join(self.host, "artifact")
        data = []
        for artifact in artifacts:
            x = dict(
                container_id=container_id,
                label=label,
                source_data_identifier=str(uuid.uuid4()),
                cef=artifact
            )
            data.append(x)

        return self.__make_rest_request__(endpoint_url,
                                          "POST",
                                          data=data)
