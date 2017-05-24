#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import json


def space_str(layer):
    spaces = "\t"
    # for i in range(0, layer):
    #     spaces += '\t'
    return spaces


def dic_to_lua_str(data, layer=0):
    # d_type = type(data)
    change_line = "\n"
    if layer > 1:
        change_line = ""
    if isinstance(data,str):
        if data.find('PUtil.get') >= 0:
            yield (data)
        else:
            yield ("'" + data + "'")
    elif isinstance(data,bool):
        if data:
            yield ('true')
        else:
            yield ('false')
    elif isinstance(data,int) or isinstance(data,float):
        yield (str(data))
    elif isinstance(data,list):
        yield ("{" + change_line)
        # yield (space_str(layer + 1))
        for i in range(0, len(data)):
            for sub in dic_to_lua_str(data[i], layer + 1):
                yield sub
            if i < len(data) - 1:
                yield (',')
        yield (change_line)
        # yield (space_str(layer))
        yield ('}')
    elif isinstance(data,dict):
        yield (change_line)
        yield (space_str(layer))
        yield ("{" + change_line)
        data_len = len(data)
        data_count = 0
        for k, v in data.items():
            data_count += 1
            # yield (space_str(layer + 1))
            try:
                k = int(k)
            except ValueError as e:
                pass
            if isinstance(k,int):
                yield ('[' + str(k) + ']')
            else:
                yield (k)
            yield (' = ')
            try:
                for sub in dic_to_lua_str(v, layer + 1):
                    yield sub
                if data_count < data_len:
                    yield (',' + change_line)

            except Exception as e:
                print('error in ', k, v)
                raise
        yield (change_line)
        # yield (space_str(layer))
        yield ('}')
    else:
        raise (type(data), 'is error')


def str_to_lua_table(jsonStr):
    data_dic = None
    try:
        data_dic = json.loads(jsonStr)
    except Exception as e:
        data_dic = []
    else:
        pass
    finally:
        pass
    bytes = ''
    for it in dic_to_lua_str(data_dic):
        bytes += it
    return bytes


