# -*- coding: cp936 -*-

"""这是第一章作业，用于多重列表的单项内容提取"""

def print_m(the_list):
        for item in the_list:
                if isinstance(item,list):
                        print_m(item)
                else:
                        print(item)

