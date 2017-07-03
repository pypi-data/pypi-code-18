# encoding: utf-8
# author: SophiaGao
'''这是try_gao_1709.py模块，它提供了一个函数print_list。这个函数能够打印列表（包括带嵌套的列表），
并且可选择是否按层次打印，也可选择是否按层次缩进。'''

def print_list(the_list, indent=False, level=0):
    '''这是print_list函数，一共有三个参数。
    the_list是当前处理的链表；indent是选择是否缩进打印，默认不缩进；
    level是缩进tab的初始个数，默认为0.'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_list(each_item, indent, level+1)
        else:
            if indent:
                for num in range(level):
                    print "\t",
            print(each_item)