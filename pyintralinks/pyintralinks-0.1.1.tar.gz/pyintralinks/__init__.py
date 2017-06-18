"""
Python Intralinks API Client
"""
import os
import json
from datetime import datetime, timedelta

import requests

DEV_URL = 'https://test-api.intralinks.com/v2'
PRD_URL = 'https://api.intralinks.com/v2'

def get_credentials(environ=None):
    """Look the current environment for Intralinks credentials """
    environment = environ or os.environ
    try:
        client_id = environment["INTRALINKS_API_CONSUMER_KEY"]
        client_secret = environment["INTRALINKS_API_CONSUMER_SECRET"]
        client_email = environment["INTRALINKS_API_EMAIL"]
        client_password = environment["INTRALINKS_API_PASSWORD"]
        return client_id, client_secret, client_email, client_password
    except KeyError:
        return None, None, None, None


class ILClient(object):
    """
    Python Intralinks API Client Class
    """
    def __init__(self,
                 dev=False,
                 email=None,
                 password=None,
                 client_id=None,
                 client_secret=None,
                 end_other_sessions=False):
        """
        Creates Intralinks REST API client
        """
        self.auth_header = None
        self.expires_in = datetime.now()

        # Get credentials from init or from environment
        if not client_id or not client_secret or not email or not password:
            client_id, client_secret, email, password = get_credentials()

        self.client_id = client_id
        self.client_secret = client_secret
        self.email = email
        self.password = password
        self.end_other_sessions = end_other_sessions

        self.base_url = PRD_URL

        if dev:
            self.base_url = DEV_URL

        if self.end_other_sessions is False:
            self.end_other_sessions = "false"
        else:
            self.end_other_sessions = "true"

    def url(self, path):
        """ Return full URL combine base and path """
        url_return = self.base_url + path
        return url_return

    def authenticate(self):
        """ Returns True if Authentication was sucessfull """
        uri = self.url('/oauth/token')
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "email": self.email,
            "password": self.password,
            "endOtherSessions": self.end_other_sessions,
        }
        now = datetime.now()
        with requests.Session() as s:
            resp = s.post(uri, data=params)
            data = json.loads(resp.content)
            access_token = data.get('access_token', None)
            expires_in = data.get('expires_in', None)
            if access_token and expires_in:
                self.auth_header = {'Authorization': "Bearer %s" % (access_token)}
                delta = timedelta(0, int(expires_in))
                self.expires_in = now + delta
                return True
        self.auth_header = None
        return False

    def workspaces(self, phase=None):
        """ Gets the list and metadata of all workspaces to which the logged-in user has access """
        uri = self.url('/workspaces')
        params = {}
        if phase:
            params = {
                'phase': phase,
            }
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header, params=params)
            data = json.loads(resp.content)
            status = data.get('status', None)
            code = status.get('code', None)
            if code == 200:
                workspace_data = data.get('workspace', None)
                return workspace_data
            else:
                return False
        return False

    def workspace(self, workspace_id):
        """ Gets the metadata of a specific workspace """
        uri = self.url('/workspaces/{}'.format(workspace_id))
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header)
            data = json.loads(resp.content)
            status = data.get('status', None)
            code = status.get('code', None)
            if code == 200:
                workspace_data = data.get('workspace', None)
                return workspace_data[0]
            else:
                return False
        return False

    def folders(self, workspace_id, root_folders=False):
        """ Gets the metadata for all folders in a workspace """
        uri = self.url('/workspaces/{}/folders'.format(workspace_id))
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header)
            data = json.loads(resp.content)
            status = data.get('status', None)
            code = status.get('code', None)
            if code == 200:
                folder_data = data.get('folder', None)
                if root_folders:
                    root_folder_list = []
                    for folder in folder_data:
                        root = folder.get('parentId', True)
                        if root is True:
                            root_folder_list.append(folder)
                    return root_folder_list
                else:
                    return folder_data
            else:
                return False
        return False


    def folder(self, workspace_id, folder_id):
        """ Gets the metadata for a specific folder """
        uri = self.url('/workspaces/{}/folders/{}'.format(workspace_id, folder_id))
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header)
            data = json.loads(resp.content)
            status = data.get('status', None)
            code = status.get('code', None)
            if code == 200:
                folder_data = data.get('folder', None)
                return folder_data[0]
            else:
                return False
        return False


    def documents(self, workspace_id):
        """ Gets the metadata for all documents in the specified workspace """
        uri = self.url('/workspaces/{}/documents'.format(workspace_id))
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header)
            data = json.loads(resp.content)
            status = data.get('status', None)
            code = status.get('code', None)
            if code == 200:
                document_data = data.get('document', None)
                return document_data
            else:
                return False
        return False

    def document(self, workspace_id, document_id):
        """ Gets the metadata of one document """
        uri = self.url('/workspaces/{}/documents/{}'.format(workspace_id, document_id))
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header)
            data = json.loads(resp.content)
            status = data.get('status', None)
            code = status.get('code', None)
            if code == 200:
                document_data = data.get('document', None)
                return document_data[0]
            else:
                return False
        return False

    def users(self, workspace_id):
        """ Gets the metadata for all Workspace Users in the specified workspace """
        uri = self.url('/workspaces/{}/users'.format(workspace_id))
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header)
            data = json.loads(resp.content)
            status = data.get('status', None)
            code = status.get('code', None)
            if code == 200:
                users_data = data.get('users', None)
                return users_data
            else:
                return False
        return False

    def groups(self, workspace_id):
        """ Gets the metadata for all Workspace Groups in the specified workspace """
        uri = self.url('/workspaces/{}/groups'.format(workspace_id))
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header)
            data = json.loads(resp.content)
            groups_data = data.get('groups', None)
            return groups_data
        return False

    def group_users(self, workspace_id, group_id):
        """ Gets the list of Workspace Users who belong to the specified Workspace Group """
        uri = self.url('/workspaces/{}/groups/{}/users'.format(workspace_id, group_id))
        now = datetime.now()
        if now >= self.expires_in:
            auth_status = self.authenticate()
            if auth_status is False:
                return False
        with requests.Session() as s:
            resp = s.get(uri, headers=self.auth_header)
            data = json.loads(resp.content)
            users_data = data.get('users', None)
            return users_data
        return False
