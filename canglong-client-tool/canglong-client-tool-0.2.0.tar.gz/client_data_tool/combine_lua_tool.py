#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author: MapzChen
# Email: 61966578@qq.com

import client_data_tool.coluaco as coluaco
import threading

def process_combine(src,dist,suffix,step_callback=None):
    t = threading.Thread(target=processCombine, args=(src,dist,suffix,step_callback))
    t.start()

def processCombine(src,dist,suffix,step_callback):
    # exportProgress("开始执行合并操作")
    try:
        coluaco.process(src,
            dist,
            None,  # build setting
            '.lua',
            "",
            None,  #in filter
            suffix, True, True,step_callback)

        return True
    except Exception as e:
        print("合并压缩操作出错，错误详情：")
        step_callback("合并压缩操作出错，错误详情："+ str(e),0,fail=True)
        return False


if __name__ == '__main__':
    def test_callback(str,progress,fail):
        print('fail:',fail)
        print('测试：',str)
        print('progress：', progress)
    processCombine('/private/var/folders/qs/wh91wz0n7gjb45htk24t7mph0000gn/T/tmp4tod4sat','/Users/mapzchen/Desktop/未命名文件夹'
    ,'.lua',test_callback)