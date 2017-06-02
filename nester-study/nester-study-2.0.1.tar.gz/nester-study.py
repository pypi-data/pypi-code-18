# -*- coding: utf-8 -*-


"""
这是nester.py模块，提供了一个名为print_lol的函数，
这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表
"""
# 定义一个列表打印函数
def print_lol(the_item):
	
	"""
	这个函数取一个位置参数，名为one_item，
	这可以是任何Python列表（也可以是包含嵌套列表的列表）。
	所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项占一行。
	"""
	
	#从one_item至the_item循环
	for one_item in the_item:
	
		#判断one_item是否为列表
		if isinstance(one_item, list):
		
			#one_item为列表时，重新调用函数print_lol()
			print_lol(one_item)
		else:
			#one_item不为列表时，循环结束并打印one_item列表内容
			print(one_item)

