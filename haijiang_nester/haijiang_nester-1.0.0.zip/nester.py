'''函数转化为模块共享'''

'''
1、模块就是一个包含Python代码的文本文件
2、文件名以py结尾
3、PyPi（python包索引，为Internet上的第三方Python模块提供了一个集中的存储库。使用PyPI发布你的模块）

'''
'''这是"nester.py"模块，提供了一个名为print_lol（）的函数，这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表'''

def print_lol(the_list):
    '''描述函数，一个处理嵌套列表的函数
      这个函数取一个位置参数，名为“the_list”,这可以是任何python列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项会占据一行
'''
    for each_movies in the_list:
        if isinstance(each_movies,list):
            print_lol(each_movies)
        else:
            print(each_movies)
