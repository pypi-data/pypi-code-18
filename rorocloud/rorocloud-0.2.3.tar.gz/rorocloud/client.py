# -*- coding: utf-8 -*-
"""
    rorocloud.client
    ~~~~~~~~~~~~~~~~

    This module provides the client interface to interact with the
    rorocloud service.

    :copyright: (c) 2017 by rorodata
    :license: Apache 2, see LICENSE for more details.
"""
from __future__ import print_function
import sys
import os
import requests
from . import __version__
from .utils import logger
from .auth import FileAuthProvider

config = {
    "ROROCLOUD_URL": "https://rorocloud.rorodata.com/"
}

class Client(object):
    """The rorocloud client.
    """
    USER_AGENT = "rorocloud/{}".format(__version__)
    HEADERS = {
        "User-Agent": USER_AGENT
    }
    AUTH_PROVIDER_CLASS = FileAuthProvider

    def __init__(self, base_url=None):
        self.base_url = base_url or self._get_config("ROROCLOUD_URL")
        self.auth_provider = self.AUTH_PROVIDER_CLASS()

    def _get_config(self, key):
        return os.getenv(key) or config.get(key)

    def _request(self, method, path, **kwargs):
        url = self.base_url.rstrip("/") + path
        auth = self.auth_provider.get_auth()
        try:
            response = requests.request(method, url,
                auth=self.auth_provider.get_auth(),
                headers=self.HEADERS,
                **kwargs)
        except requests.exceptions.ConnectionError:
            raise ClientError("ERROR: Unable to connect to the rorocloud server.")

        return response

    def get(self, path):
        return self._request("GET", path)

    def post(self, path, data):
        logger.debug("data %s", data)
        return self._request("POST", path, json=data)

    def delete(self, path):
        return self._request("DELETE", path)

    def jobs(self, all=False):
        if all:
            response = self.get("/jobs?all=true")
            if response.status_code != 200:
                return self.handle_error(response)
            return [Job(job) for job in response.json()]
        else:
            response = self.get("/jobs")
            if response.status_code != 200:
                return self.handle_error(response)
            return [Job(job) for job in response.json()]

    def get_job(self, job_id):
        path = "/jobs/" + job_id
        response = self.get(path)
        if response.status_code != 200:
            return self.handle_error(response)
        return Job(response.json())


    def get_logs(self, job_id):
        path = "/jobs/" + job_id + "/logs"
        response = self.get(path)
        if response.status_code != 200:
            return self.handle_error(response)
        return response.json()

    def stop_job(self, job_id):
        path = "/jobs/" + job_id
        response = self.delete(path)
        if response.status_code != 200:
            return self.handle_error(response)

    def run(self, command, workdir=None, shell=False, instance=None, docker_image=None):
        details = {}
        if workdir:
            details['workdir'] = workdir
        payload = {
            "command": list(command),
            "instance_type": instance,
            "details": details
        }
        if 'docker_image':
            payload['details']['docker_image'] = docker_image
        response = self.post("/jobs", payload)
        if response.status_code != 200:
            return self.handle_error(response)
        return Job(response.json())

    def login(self, email, password):
        payload = {"email": email, "password": password}
        response = self.post("/login", payload)
        if response.status_code != 200:
            return self.handle_error(response)
        data = response.json()
        if "token" not in data:
            raise UnAuthorizedException()
        self.auth_provider.set_auth(email, data['token'])

    def put_file(self, source, target):
        payload = open(source, 'rb')
        files = { 'file': payload }
        response = self._request("POST", "/upload?path="+target, files=files)
        if response.status_code != 200:
            return self.handle_error(response)
        return response.json()

    def whoami(self):
        response = self.get("/whoami")
        if response.status_code != 200:
            return self.handle_error(response)
        return response.json()

    def handle_error(self, response):
        try:
            error_message = response.json()['error']
        except ValueError:
            error_message = 'unable to complete the request due to internal server error'
        raise ClientError(error_message)

class Job(object):
    def __init__(self, data):
        self.data = data
        self.id = data['jobid']
        self.status = data['status']
        self.command_args = data['details']['command']
        self.command = " ".join(self.command_args)
        self.status = data["status"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
        self.instance_type = data.get("instance_type")

class UnAuthorizedException(Exception):
    pass

class ClientError(Exception):
    pass
