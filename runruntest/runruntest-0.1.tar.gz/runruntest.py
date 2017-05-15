"""
该模块提供一个方法
print_lists来打印列表(无论是否内嵌列表)
"""


def print_lists(the_list):
    """
    打印列表
    :param the_list: 
    :return: 
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lists(each_item)
        else:
            print(each_item)
