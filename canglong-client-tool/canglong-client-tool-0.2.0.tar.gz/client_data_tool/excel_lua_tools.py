#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: MapzChen
# Email: 61966578@qq.com

import json
import os
import os.path
import re
import threading

import xlrd

from client_data_tool.json_to_lua import str_to_lua_table


class ExcelToLua():
    use_thread = True

    def __init__(self, input_file_list,output_dist):
        self.input_file_list = input_file_list
        self.output_dist = output_dist
        self.process_over_list = {}
        self._threads = []
        self.one_file_callback = None
        self.process_over_callback = None
        self.progress_status = "OK"

    def set_callback(self,one_file_callback = None,process_over_callback = None):
        self.one_file_callback = one_file_callback if self.one_file_callback == None else self.one_file_callback
        self.process_over_callback = process_over_callback if self.process_over_callback == None else self.process_over_callback

    def start_process(self):
        print('开始处理文件列表')
        print('文件列表：',self.input_file_list)
        for file_path in self.input_file_list:
            if self.use_thread:
                t = threading.Thread(target=self._start_parse_file,args=(file_path,))
                # t.setDaemon(True)
                t.start()
            else:
                self._start_parse_file(file_path)


    def _start_parse_file(self,file_path):
        print('处理文件：',file_path)
        result,status_text = self.parse_file(file_path,self.output_dist)
        if not result:
            self.progress_status = "FAILED"
        self.process_over_list[file_path] = {'result':result,'status_text':status_text}
        self._parse_callback(file_path,result,status_text)


    def _parse_callback(self,file_path,result,status_text):
        print('处理文件完成：', file_path)
        progress = len(self.process_over_list)/len(self.input_file_list)
        print('处理进度：', progress)
        if self.one_file_callback:
            self.one_file_callback(file_path,progress,result,status_text)
        if progress == 1 and self.process_over_callback:
            self.process_over_callback(self.process_over_list)

    @staticmethod
    def parse_folder(folder_path,dist_path,process_over_callback = None,one_file_callback = None):
        list_for_process = []
        for parent,dirname,filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.find('xls') > 0 and filename.find('~$') < 0:
                    list_for_process.append(os.path.join(folder_path,filename))

        if len(list_for_process) > 0:
            process = ExcelToLua(list_for_process, dist_path)
            process.set_callback(process_over_callback=process_over_callback,one_file_callback=one_file_callback)
            process.start_process()
        else:
            return False

    @staticmethod
    def parse_file(file_path,dist_path):
        try:
            ExcelToLua._process_file(file_path,dist_path)
        except Exception as e:
            print(file_path + " : " + e.__str__())
            return False,file_path + " : " + e.__str__()
        return True,'完成处理：' + file_path

    @staticmethod
    def _process_file(file_path,dist_path):
        data = xlrd.open_workbook(file_path)
        table = data.sheet_by_index(0)
        file_name = file_path[file_path.rfind('/') + 1:file_path.rfind('.')]
        output_name = file_name + 'ClientData'
        output_file_name = output_name + '.lua'

        # 处理表头
        head = table.row_values(0)
        column_table = {}
        for index, head_str in enumerate(head):
            match = re.compile('\((.*)\)')
            find_lua_head = match.findall(head_str)
            if len(find_lua_head) == 0:
                continue
            find_lua_head = find_lua_head[0]
            find_title = find_lua_head.split(',')
            if len(find_title) == 1:
                column_table[index] = {'v_type':'id'}
            elif len(find_title) == 2:
                column_table[index] = {'v_type':find_title[0],'v_name':find_title[1]}

        # 处理表内容
        data = {
            output_name:{}
        }
        total_rows = table.nrows
        for row_index in range(1,total_rows):
            row_data = {}
            # print(row_index)
            for col_index,col_params in column_table.items():
                cell_value = table.cell(row_index, col_index).value
                cell_type = col_params['v_type']
                if cell_type == "id":
                    data[output_name][int(cell_value)] = row_data
                elif cell_type == "num":
                    if isinstance(cell_value,str):
                        # 判断为值为列表的情况
                        match = re.compile('\{(.*)\}')
                        find_list = match.findall(cell_value)
                        if len(find_list) > 0:
                            find_list = find_list[0].split(',')
                            for index, item in enumerate(find_list):
                                try:
                                    find_list[index] = float(item)
                                    if find_list[index] % 1 == 0:
                                        find_list[index] = int(find_list[index])
                                except ValueError:
                                    if len(item) == 0:
                                        find_list = []
                            cell_value = find_list
                    else:
                        cell_value = float(cell_value)
                        if cell_value % 1 == 0:
                            cell_value = int(cell_value)
                elif cell_type == "str":
                    if isinstance(cell_value,float):
                        if cell_value % 1 == 0:
                            cell_value = int(cell_value)
                        cell_value = str(cell_value)

                    match = re.compile('\{(.*)\}')
                    find_list = match.findall(cell_value)
                    if len(find_list) > 0:
                        find_list = find_list[0].split(',')
                        for index, item in enumerate(find_list):
                            try:
                                find_list[index] = float(item)
                                if find_list[index] % 1 == 0:
                                    find_list[index] = int(find_list[index])
                            except ValueError:
                                if len(item) == 0:
                                    find_list = []
                        cell_value = find_list
                elif cell_type == "fun":
                    if isinstance(cell_value,str):
                        # 判断为值为列表的情况
                        match = re.compile('\{(.*)\}')
                        find_list = match.findall(cell_value)
                        if len(find_list) > 0:
                            find_list = find_list[0].split(',')
                            for index, item in enumerate(find_list):
                                try:
                                    find_list[index] = float(item)
                                    if find_list[index] % 1 == 0:
                                        find_list[index] = int(find_list[index])
                                except ValueError:
                                    if len(item) == 0:
                                        find_list = []
                            cell_value = find_list
                if isinstance(cell_value,str):
                    if len(str.strip(cell_value)) == 0:
                        cell_value = None

                if col_params['v_type'] != 'id':
                    if cell_value:
                        row_data[col_params['v_name']] = cell_value

        # print(data)

        lua_str = str_to_lua_table(json.dumps(data))

        lua_str = lua_str[lua_str.find('{') + 1:lua_str.rfind('}')]

        with open(dist_path + '/' + output_file_name, 'w',encoding='utf-8') as luafile:
            luafile.write(lua_str)

        return True

'''
0 = {str} '编号(idx){id,int}'
1 = {str} '宝箱ID{boxId,int}(num,boxId)'
2 = {str} '道具类型{gtype,int}(num,gtype)'
3 = {str} '道具ID{cid,int}(num,cid)'
4 = {str} '道具数量{number,ints}(num,shuliang)'
5 = {str} '道具几率{rate,int}'
6 = {str} ''
7 = {str} ''
8 = {str} '辅助列'
'''

if __name__ == '__main__':
    # test_list = [
    #     '/Volumes/store/sanguoXM/svnFolder/document/三国竖版配置档/东南亚版本/三国东南亚_配置表_XLS/Chest.xlsx',
    #     '/Volumes/store/sanguoXM/svnFolder/document/三国竖版配置档/东南亚版本/三国东南亚_配置表_XLS/Hero.xlsx',
    #     '/Volumes/store/sanguoXM/svnFolder/document/三国竖版配置档/东南亚版本/三国东南亚_配置表_XLS/Propertites.xlsx',
    #     '/Volumes/store/sanguoXM/svnFolder/document/三国竖版配置档/日本版本/三国日文版_配置表_XLS/Propertites.xlsx',
    # ]

    # x = [ str(y) for y in range(200)]
    # process = ExcelToLua(test_list,'/Users/mapzchen/Desktop/testfolder')
    # process.set_callback(process_over_callback=lambda list: [print(i) for i in list])
    # process.start_process()
    # ExcelToLua.parse_file('','x')

    ExcelToLua.parse_folder('/Volumes/store/sanguoXM/svnFolder/document/三国竖版配置档/日本版本/三国日文版_配置表_XLS/','/Users/mapzchen/Desktop/testfolder')

