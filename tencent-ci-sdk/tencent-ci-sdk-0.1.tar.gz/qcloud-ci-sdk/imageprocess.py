# -*- coding: utf-8 -*-

import os.path
import time
import urllib
import json
import requests
from tencentyun import conf
from .auth import Auth

class ImageProcess(object):

    def __init__(self, appid, secret_id, secret_key, bucket):
        self.IMAGE_FILE_NOT_EXISTS = -1
        self._secret_id,self._secret_key = secret_id,secret_key
        conf.set_app_info(appid, secret_id, secret_key, bucket)

    def porn_detect(self, porn_detect_url):
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.get_porn_detect_sign(porn_detect_url)
        app_info = conf.get_app_info()

        if False == sign:
            return {
                'code':9,
                'message':'Secret id or key is empty.',
                'data':{},
            }

        url = app_info['end_point_porndetect']
        payload = {
            'bucket':app_info['bucket'],
            'appid':int(app_info['appid']),
            'url':(porn_detect_url).encode("utf-8"),
        }
        header = {
            'Authorization':sign,
            'Content-Type':'application/json',
        }
        r = {}
        r = requests.post(url, data=json.dumps(payload), headers=header)
        ret = r.json()

        return ret
        
    def porn_detect_url(self, porn_url):
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.get_porn_detect_sign()
        app_info = conf.get_app_info()

        if False == sign:
            return {
                'code':9,
                'message':'Secret id or key is empty.',
                'data':{},
            }

        url = app_info['end_point_porndetect']
        payload = {
            'bucket':app_info['bucket'],
            'appid':int(app_info['appid']),
            'url_list':porn_url,
        }
        header = {
            'Authorization':sign,
            'Content-Type':'application/json',
        }
        r = {}
        r = requests.post(url, data=json.dumps(payload), headers=header)
        ret = r.json()

        return ret

    def porn_detect_file(self, porn_file):
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.get_porn_detect_sign()
        app_info = conf.get_app_info()

        if False == sign:
            return {
                'code':9,
                'message':'Secret id or key is empty.',
                'data':{},
            }

        url = app_info['end_point_porndetect']
        header = {
            'Authorization':sign,
        }
        files = {
            'appid':(None,app_info['appid'],None),
            'bucket':(None,app_info['bucket'],None),
        }
        i=0
        for pfile in porn_file:
            pfile = pfile.decode('utf-8')
            local_path = os.path.abspath(pfile)
            if not os.path.exists(local_path):
                return {'httpcode':0, 'code':self.IMAGE_FILE_NOT_EXISTS, 'message':'file ' + pfile + ' not exists', 'data':{}}
            i+=1
            files['image['+str(i-1)+']']=(pfile, open(pfile,'rb'))

        r = requests.post(url, headers=header, files=files)
        ret = r.json()

        return ret
