#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author: MapzChen
# Email: 61966578@qq.com


a = '/Volumes/store/sanguoXM/svnFolder/document/三国竖版配置档/东南亚版本/三国东南亚_配置表_XLS/Chest.xlsx'

print(a[a.rfind('/') + 1:a.rfind('.')])

print(isinstance(a,str))

print('PUtil.get(531065)'.find('PUtil.get1'))