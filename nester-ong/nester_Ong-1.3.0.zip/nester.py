# -*- coding: cp936 -*-

"""这是第一章作业，用于多重列表的单项内容提取"""

def print_m(the_list,indent=False,level=0):
        for item in the_list:
                if isinstance(item,list):
                        print_m(item,indent,level+1)
                else:
                        if indent:
                          for tab_stop in range(level):
                             print"\t",
                        print(item)



