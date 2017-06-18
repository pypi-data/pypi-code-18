#encoding:utf-8
import sys
"""这是 “nester.py”模块，提供了一个 名为 printlol()的函数，这个函数的作用是打印列表，其中有可能（也可能不包含）嵌套列表"""
def print_lol(the_list,indent=False,level=0,fn=sys.stdout):
	""""这个函数有一个位置参数，名为“the_list”,这可以是任何python列表,也可以包含嵌套列表的列表。
		indent参数为bool类型，用于指示是否缩进打印列表
		level指示预订缩进值
		所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项各占一行
		fn参数用于指定打印输出文件位置 """
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1,fn)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",file=fn),
			print(each_item,file=fn)

