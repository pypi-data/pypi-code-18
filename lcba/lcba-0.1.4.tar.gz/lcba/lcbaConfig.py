#!/usr/bin/env python
# coding: utf-8

#常量: 生成apk的编译命令
BUILD_APK_TASK = "assembleRelease"

#for lint
#常量: 生成lint报告的文件
LINT_RESULT_PATH = "build/reports/lint-results.xml"
#常量: 生成lint 报告的命令
TASK_LINT = "lint"
#常量: android sdk
ANDROID_SDK = "/Users/tory/Library/Android/sdk/"
#常量: 忽略无用的布局文件
IGNORE_LAYOUTS_FILE = False
#常量: 忽略布局文件里面的内容，不要该成False！！！
IGNORE_LAYOUTS_VALUE = True
#常量: 解决布局文件中被删除的文件中含有@+id，被其他文件@id引用的情况
LAYOUT_IDS_PATH = "src/main/res/values/lint_ids.xml"
#常量: 自定义信号，服务器未lint错误
SERVER_LINT_ERROR = 100
#常量: 自定义信号，服务器未压缩错误
SERVER_COMPRESS_ERROR=101


#for compressPng
#常量: 服务器最大容错次数
MAX_SERVER_ERROR_COUNT = 3
#常量: 图片最大容错次数
MAX_PIC_ERROR_COUNT = 3
#常量:账号列表
API_KEY_LIST = [
    "sXzp30KfRZaf0NlWaQP0U3qEwQwoCl7s",#use feiy1@jumei.com register
    "l1og95PkmrPVMpf2NMSjnEmtwIL6urf1",#use xiaomom@jumei.com register
    "QfjLJJNOSShBxWtE1-tUC9Bfjg6U9Om3",#use xiaojiangk@jumei.com register
    "WaNaNSYc84TNr8DZpgZFRo8QnxhSaV3L",#use hongc@jumei.com register
    "tdSdRzIvicVO3oTfrXZ6374P7uyBx-Kf",#use changqiangl@jumei.com register
    "Jltmnr4b7xkQedUyiza-v12FZpIOPG8O",#use test1_jumei@mail.com register
    "tFrVjiAQyYshUKvGDGuCZZa0cmW_VuM9",#use xiangc register
]

#常量: md5 文件名称
PIC_MD5_FILE_NAME = "_md5.txt"
MODULES_NAME = [
    'app',
    'jmwebsocketsdk',
    #'baselib',#lint 的时候有依赖baselib，但是它在模块内未使用
]


#for andRes
#常量: zipalign PATH
ZIPALIGN_PATH = ANDROID_SDK+"build-tools/25.0.1/zipalign"
#常量: 生成apk的编译命令
BUILD_APK_PATH = "build/outputs/apk/app-release.apk"
ANDROID_MANIFEST_FILE = "src/main/AndroidManifest.xml"