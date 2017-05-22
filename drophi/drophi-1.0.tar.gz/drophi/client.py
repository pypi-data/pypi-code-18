import urllib.parse

import requests_unixsocket

class CommunicationError(Exception):
    "Parent class for any communications errors with Docker"

class Client():
    def __init__(self):
        self.session = requests_unixsocket.Session()

    def _path(self, path):
        socket = urllib.parse.quote('/var/run/docker.sock', safe='')
        return 'http+unix://{}{}'.format(socket, path)

    def _get(self, path):
        url = self._path('/containers/json')
        response = self.session.get(url)
        if not response.ok:
            raise CommunicationError("Failed to communicate with docker: status {} content {}".format(
                response.status_code,
                response.text,
            ))
        data = response.json()
        return data

    def ps(self):
        return self._get('/containers/json')
