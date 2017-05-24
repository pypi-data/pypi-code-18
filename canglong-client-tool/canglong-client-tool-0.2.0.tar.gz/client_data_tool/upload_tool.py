#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author: MapzChen
# Email: 61966578@qq.com

import paramiko
import os
import threading
'''
config : {
    remote_sftp_ip:xx,
    remote_sftp_port:xx,
    user_name:xxx,
    password:xxx,
    profiles:[
        {
            remote_path:xxx,
            suffix:.lua,
        },
        {},
        ...
    ]

}
'''

class UploadTool():
    def __init__(self,config,src_path,callback):
        self.config = config
        self.callback = callback
        self.src_path = src_path

        self.files = [
            "clientDataConfig",
            # "RefineClientData"
        ]

    def _process_upload(self):
        port = self.config.get("remote_sftp_port",None)
        if port:
            t = paramiko.Transport((self.config.get("remote_sftp_ip"), port))
        else:
            t = paramiko.Transport((self.config.get("remote_sftp_ip")))
        # t.connect(username="honor", password="zK2p@dM$bh")
        t.connect(username=self.config.get("user_name"),password=self.config.get("password"))
        sftp = paramiko.SFTPClient.from_transport(t)

        profiles = self.config.get('profiles')
        for profile in profiles:
            remote_path = profile.get('remote_path')
            suffix = profile.get('suffix')

            for i,file_name in enumerate(self.files):
                remote = remote_path + file_name + '.lua'
                localpath = self.src_path + os.sep + file_name + suffix
                self.callback('上传: ' + localpath + '到:' + remote,i/len(self.files),fail = False)
                sftp.put(localpath, remote)

        self.callback('上传: ' + localpath + '到:' + remote, 1,fail = False)

    def process_upload(self):
        try:
            t = threading.Thread(target=self._process_upload)
            t.start()
        except Exception as e:
            print(str(e))
            self.callback('上传失败:' + str(e), 1, fail=True)


if __name__ == '__main__':
    def test_callback(str,progress,fail):
        print('fail:',fail)
        print('测试：',str)
        print('progress：', progress)


    # upload = UploadTool(,
    #     '/Users/mapzchen/Desktop/testfolder',
    #     test_callback
    #     )
    #
    # upload.process_upload()
