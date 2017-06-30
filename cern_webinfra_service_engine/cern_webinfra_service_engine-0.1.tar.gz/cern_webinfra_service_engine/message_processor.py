import json
import re
from abc import ABCMeta
from .exceptions import MethodNotAllowed, RouteNotSpecified


class MessageProcessor(metaclass=ABCMeta):
    def __init__(self, conn):
        self.queue_connection = conn
        self.routes = {}

    def process(self, headers, message):
        m = json.loads(message)
        method = m['http_method']
        params, resource = self._get_route(m['path'])

        if method == 'POST':
            resource.post(self, params)
        elif method == 'PUT':
            resource.put(self, params)
        elif method == 'DELETE':
            resource.delete(self, params)
        else:
            raise MethodNotAllowed(method)

    def add_resource(self, resource, paths):
        for path in paths:
            self.routes[
                self._get_path_pattern(path)
            ] = resource

    @staticmethod
    def _get_path_pattern(path):
        return re.compile("^{}$".format(
            re.sub(r'(<\w+>)', r'(?P\1.+)', path))
        )

    def _get_route(self, path):
        for route in self.routes.keys():
            m = route.match(path)
            if m:
                return m.groupdict(), self.routes[route]
        raise RouteNotSpecified(path)

    def _acknowledge(self, message_id):  # TODO
        self.update_request_status()
        self.queue_connection.ack(
            message_id.ack()
        )

    def update_request_status(self):
        pass  # TODO
