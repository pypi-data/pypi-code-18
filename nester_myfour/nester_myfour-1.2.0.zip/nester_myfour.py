"""
这是一个模块，提供了一个名为print_lol的函数，该函数能打印嵌套列表
"""


def print_lol(the_list,level=0):
    """

    :param the_list:
    :return:
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print('\t', end='')
            print(each_item)
