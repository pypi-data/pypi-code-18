#!/usr/bin/env python             
# coding: utf-8
#####使用字典来对全局跨文件的变量进行访问
import os
import lcbaUtil as util
import lcbaConfig as config

WORK_PATH="work_path"
MODULES_NAME="modules_name"
LCBA_PATH="lcba_path"
GRADLEW_PATH="gradle_path"
BUILD_ON_SERVER="build_on_server"

_global_dict = {}

def set_value(key,value):
    """ 定义一个全局变量 """
    # getValue(key,value)
    _global_dict[key] = value


def get_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue

def getValue(key,defValue=None):
    ret = None
    try:
       ret = get_value(key,None)
    except NameError:
        pass
    if not ret:
        initModules()
        ret = get_value(key,defValue)
    pass
    return ret
pass

def initModules():
    curPath=os.getcwd()
    print curPath
    curPath=curPath.replace('lcba','')

    workPath = None
    for dirpath, dirnames, filenames in os.walk(curPath):
        #print dirpath
        for filename in filenames:
            #print filename
            if filename == 'settings.gradle':
                if dirpath.endswith('/'):
                    workPath = dirpath[0:len(dirpath)-1]
                else:
                    workPath = dirpath
                print "find root work path:%s"%workPath
                break
            pass
        pass
    pass

    if None == workPath:
        print "initModules()...not find work path!!!"
        util.safeQuit(None, None)
    pass

    set_value(WORK_PATH,workPath)
    lcbaDirPath=os.path.join(workPath,"lcba")
    if os.path.exists(lcbaDirPath):
        set_value(LCBA_PATH,lcbaDirPath)
    pass
    gradlewPath=os.path.join(workPath,"gradlew")
    if os.path.exists(gradlewPath):
        set_value(GRADLEW_PATH,gradlewPath)
    pass
    modules_name = []
    ##方案一，从目录的settings.gradle 中读取有多少个模块，缺点,在lint的时候被依赖的模块资源会被删除
    # with open(workPath+"settings.gradle") as f:
    #     for line in f.readlines():
    #         if line.startswith('//') or '#' in line:
    #             continue
    #         pass
    #         pattern = re.compile('\':\\b[^\']+')
    #         match_result=re.findall(pattern,line)
    #         if match_result:
    #             for item in match_result:
    #                 bits=item.rsplit(':',2)
    #                 #print bits[1]
    #                 moduleFile=curPath+"/"+bits[1]
    #                 if not os.path.exists(moduleFile):
    #                     os.makedirs(r'%s'%moduleFile)
    #                     print "create module dir:%s"%moduleFile
    #                 pass
    #                 modules_name.append(bits[1])
    #             pass
    #         pass
    #     pass
    # pass

    ##方案二自己添加
    # modules_name.append('app')
    # modules_name.append('jmwebsocketsdk')
    modules_name.extend(config.MODULES_NAME)

    set_value(MODULES_NAME,modules_name)
pass