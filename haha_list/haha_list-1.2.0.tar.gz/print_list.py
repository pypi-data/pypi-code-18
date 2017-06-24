#encoding=utf8

"""这是print_list模块，提供了一个名为print_list()的函数，这个函数的作用是打印列表，其中有可能包含嵌套列表"""

def print_list(lists,open=False,level=0):
    """这个函数取一个位置参数，名为lists，这可以是任何python列表（也可以是包含嵌套列表的列表），所指定的列表中的每个数据项会
    （递归的）输出到屏幕上，各数据项占一行"""
    for each_item in lists:
        if isinstance(each_item,list):
            print_list(each_item,open,level+1)
        else:
            if open:
                for tab in range(level):
                    print("\t",end="")
            print(each_item)

