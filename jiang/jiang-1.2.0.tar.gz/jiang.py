#import jiang(如果有import的话会执行一遍jiang.py中的所有代码，输出结果，这个py中只有movies时引入会把模块函数引入进来。)
""" 这是"wester.py" 模块， 提供了一个名为print_lol()的函数，这个函数的作用是打印列表，其中有可能包含(也可能不包含)嵌套列表。 """
def print_lol(the_list, level):
	""" 这个函数取一个位置参数，名为"the_list"，这可以是任何python列表(也可以是包含嵌套列表的列表)。所指定的列表中的每个数据项会(递归地)输出到屏幕上，格数据项各占一行。 """
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, level+1)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(each_item)


movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
           ["Graham Chapman", 
           		["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]
           ]
		 ]

#print_lol(movies)
#jiang.print_lol(movies, 1)