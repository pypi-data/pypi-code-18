#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
use me to get the config of xdiamond
'''
#############################################
# Author: locke
# Mail: lockeCucumber@163.com
# Created Time:  2017-06-21 14:16:16
#############################################
import json
import os
import requests


class Client(object):
    '''the client of xdiamond'''

    def __init__(self, host, port, group_id, artifact_id, version):
        self.host = host
        self.port = port
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version


class Profile(object):
    '''the profile of client'''

    def __init__(self, client, profile_name, secret_key,
                 profile_name_back='base', secret_key_back=''):
        self.client = client
        self.profile_name = profile_name
        self.secret_key = secret_key
        self.profile_name_back = profile_name_back
        self.secret_key_back = secret_key_back


    def get_config(self, config_key):
        '''get the config'''
        url = "http://{0}:{1}/clientapi/config?groupId={2}" \
              "&artifactId={3}&version={4}&profile={5}&secretKey={6}" \
              "&format=json".format(self.client.host, str(self.client.port),
                                    self.client.group_id, self.client.artifact_id,
                                    self.client.version, self.profile_name, self.secret_key)
        response = requests.get(url)
        if response.status_code == 200:
            res_json = json.loads(response.content)
            config_list = [item['config'] for item in res_json]
            config_dic = {config['key']: config['value'] for config in config_list}
            return config_dic[config_key]
        else:
            url = "http://{0}:{1}/clientapi/config?groupId={2}" \
              "&artifactId={3}&version={4}&profile={5}&secretKey={6}" \
              "&format=json".format(self.client.host, str(self.client.port),
                                    self.client.group_id, self.client.artifact_id,
                                    self.client.version, self.profile_name_back, self.secret_key_back)
            response = requests.get(url)
            if response.status_code == 200:
                res_json = json.loads(response.content)
                config_list = [item['config'] for item in res_json]
                config_dic = {config['key']: config['value'] for config in config_list}
                return config_dic[config_key]


if __name__ == '__main__':
    client = Client('119.29.70.120', 11111, 'data', 'bi', '1.0')
    profile = Profile(client, 'bae', 'fsd')
    print profile.get_config('odoo_db_user')
