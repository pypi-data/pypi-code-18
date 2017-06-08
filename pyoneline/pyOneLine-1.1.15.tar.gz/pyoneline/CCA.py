#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 15:46:49 2017

@author: zhoumingzhen
"""
import json
import requests
from math import * 
import time
import random
    
def _BdCMer(BDcoor):
    """
    mercator = {"x":12940638.98, "y":4838339.82} 
    lonlat = {} 
    lonlat['x'] - mercator['x']/ 20037508.3427892 * 180 = 0
    lonlat['y'] - 180 / math.pi * (2 * math.atan(math.exp((mercator['y']/ 20037508.3427892 * 180) * math.pi / 180)) - math.pi / 2) = 0
    print (lonlat)
    """
    Merx = BDcoor[0]*20037508.34/180
    Mery = log(tan((90 + BDcoor[1])*pi/360))/(pi/180)
    Mery = Mery*20037508.34/180
    return Merx,Mery
def addr(BDcoor):
    Merx,Mery = _BdCMer(BDcoor)
    param0 = str(Merx) + ',' + str(Mery)
    #param1 = str(Merx-484) + ',' + str(Mery-333)
    #param2 = str(Merx+484) + ',' + str(Mery-333)
    timeStamp = str(time.time()).replace(".", "")[:13]
    params = {
            "newmap" : "1",
            "reqflag" : "pcmap",
            "biz" : "1",
            "from" : "webmap",
            "da_par" : "direct",
            "pcevaname" : "pc4.1",
            "qt" : "s",
            "from" : "webmap",
            "da_src":"searchBox.button",
            "wd" : "",
            "c" : "",
            "src" : "0",
            "wd2" : "",
            "l" : "18",
            "b" : "("+param0+";"+param0+")",
            "from":"webmap",
            "biz_forward":"{%22scaler%22:1,%22styles%22:%22pl%22}",
            "sug_forward":"",
            "tn":"B_NORMAL_MAP",
            "nn":"0",
            "u_loc" : param0,
            "ie" : "utf-8",
            "t" : timeStamp
            }
        
    ajaxquery="http://map.baidu.com/"
    response=requests.get(ajaxquery,params=params)
    result = json.loads(response.text)    
    #print(result)
    current_city = result['current_city']
    return (current_city['up_province_name'],current_city['name'])

def detaddr(BDcoor):
    Merx,Mery = _BdCMer(BDcoor)
    rand1 = random.randint(1,10)
    rand2 = random.randint(10,20)
    params = {
            "qt":"rgc",
            "x":"%.2f" %Merx,
            "y":"%.2f" %Mery,
            "dis_poi":rand1,
            "poi_num":rand2,
            "ie":"utf-8",
            "oue":"1",
            "fromproduct":"jsapi",
            "res":"",
            "callback":"" 
            }    
    ajaxquery="http://api.map.baidu.com/"
    response=requests.get(ajaxquery,params=params)
    result = json.loads(response.text)
    detaddr = result['content']['address'] 
    return detaddr
# http://api.map.baidu.com/?qt=rgc&x=12952036.89&y=4838678.38&dis_poi=100&poi_num=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk16238&ak=E4805d16520de693a3fe707cdc962045                                                                                                                                                            

if __name__ == '__main__':
    BDcoor = (123.325, 45)
    print(addr(BDcoor))
    print(detaddr(BDcoor))
