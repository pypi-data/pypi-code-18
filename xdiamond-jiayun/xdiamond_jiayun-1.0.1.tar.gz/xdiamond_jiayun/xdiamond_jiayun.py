#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# Author: locke
# Mail: lockeCucumber@163.com
# Created Time:  2017-06-21 14:16:16
#############################################
import requests
import json
import os


base_dir = os.path.dirname(os.path.realpath(__file__))
config_file = base_dir + '/xDiamond.config'


def get_config(group_id, artifact_id, version, profile, secret_key, config_key):
    url = "http://119.29.70.120:11111/clientapi/config?groupId={0}&artifactId={1}&version={2}&profile={3}&secretKey={4}&format=json".format(
          group_id, artifact_id, version, profile, secret_key)
    response = requests.get(url)
    if response.status_code == 200:
        res_json = json.loads(response.content)
        config_list = [item['config'] for item in res_json]
        config_dic = {config['key']:config['value'] for config in config_list}
        if not os.path.exists(config_file):
            with open(config_file, mode='a') as f:
                for k,v in config_dic.items():
                    f.write(k + '=' + v +'\n')
        else:
            os.remove(config_file)
            with open(config_file, mode='a') as f:
                for k,v in config_dic.items():
                    f.write(k + '=' + v +'\n')
        return config_dic[config_key]
    else:
        with open(config_file, mode='rU') as f:
            config_dic = {line.strip().split('=')[0]:line.strip().split('=')[1] for line in f.readlines()}
            return config_dic[config_key]
