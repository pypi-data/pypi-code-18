#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""    
    2015/10/14  WeiYanfeng
    公共函数 包

~~~~~~~~~~~~~~~~~~~~~~~~
共函数 包
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install redis

"""

from python_version import IsPython3OrLater

if IsPython3OrLater():
    __all__ = ["WyfPublicFuncs", "CLogTagMsg", "CPickleDict",
               "CSendSMTPMail", "CSendCustomMsgWX",
               "CHttpJsonClient",
               "WyfSupplyFuncs", "WyfQueueThread",
               "CHandleCmd_BaseService"]

else:
    from WyfPublicFuncs import GetCurrentTime,GetUnixTimeStr,GetUnixTimeLocal,GetLocalTime,GetYYYYMMDDhhnnss,\
        GetCurrentTimeMS,GetCurrentTimeMSs,GetTimeInteger,GetTimeIntMS,GetTimeStampIntFmYMDHns

    from WyfPublicFuncs import YMDhnsAddSeconds,AddSubMonthYYYYMM,AddSubDayYYYYMMDD
    from WyfPublicFuncs import ReturnWeekDayFmYMD,ReturnWeekNumFmYMD

    from WyfPublicFuncs import PrintInline,PrintNewline,PrintTimeMsg,PrintfTimeMsg,PrintMsTimeMsg,PrintAndSleep,\
        LoopPrintSleep,PrettyPrintObj,PrettyPrintStr,printCmdString,printHexString,IsUtf8String,IsValueString

    from WyfPublicFuncs import GetRandomInteger,ConvertStringToInt32,GetCodeFmString,crc32,md5,md5file

    from WyfPublicFuncs import GetSrcParentPath,GetCriticalMsgLog,CAppendLogBase,WyfAppendToFile
    from CLogTagMsg import CLogTagMsg
    from WyfPublicFuncs import JoinGetFileNameFmSrcFile
    from WyfPublicFuncs import RequestsHttpGet,RequestsHttpPost
    from WyfPublicFuncs import CatchExcepExitTuple,CatchExcepExitParam

    from WyfPublicFuncs import ClassForAttachAttr
    from WyfPublicFuncs import GetSystemPlatform
    from WyfPublicFuncs import ReadTailLines,ReadLargeFileDo,GetFileSizeModTime

    from CPickleDict import CPickleDict

    from CSendSMTPMail import CSendSMTPMail
    from CSendCustomMsgWX import CSendCustomMsgWX

    from CSerialJson import CSerialJson
    from CHttpJsonClient import CHttpJsonClient

    from SimpleShiftEncDec import SimpleShiftEncode,SimpleShiftDecode

    from WyfSupplyFuncs import get_total_size
    from WyfQueueThread import StartThreadDoSomething, CThreadCacheByQueue, CThreadDiscardDeal

    # from JsonRpcFuncs import # WeiYF.20161206 该单元暂保留，不输出
    # WeiYF.20170605 将 redis 相关封装转移到 weberRedis 包
    # from CRedisSubscribe import GetRedisClient,CRedisSubscribe,RedisPipeWatchExec
    # from CAutoConnectRedis import CAutoConnectRedis

    from CHandleCmd_BaseService import RegisterForHandleCmdService, CHandleCmd_BaseService

if __name__ == '__main__':
    PrintTimeMsg("Just print something!")