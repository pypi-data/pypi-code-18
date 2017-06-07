'''函数转化为模块共享'''

'''
1、模块就是一个包含Python代码的文本文件
2、文件名以py结尾
3、PyPi（python包索引，为Internet上的第三方Python模块提供了一个集中的存储库。使用PyPI发布你的模块）

修改：添加第四个参数，用来表示将把数据写入哪个位置。注：一定要为这个参数提供一个缺省值sye.stdout,
'''
'''这是"nester.py"模块，提供了一个名为print_lol（）的函数，这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表'''

import sys


def print_lol(the_list,indent=False,level=0,fn=sys.stdout):
    '''描述函数，一个处理嵌套列表的函数
      这个函数取一个位置参数，名为“the_list”,这可以是任何python列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项会占据一行
      第二个参数（名为“level”）用来在遇到嵌套列表时插入制表符。
'''
    for each_movies in the_list:
        if isinstance(each_movies,list):
            print_lol(each_movies,indent,level+1,fn)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='',file=fn)
            print(each_movies,file=fn)
