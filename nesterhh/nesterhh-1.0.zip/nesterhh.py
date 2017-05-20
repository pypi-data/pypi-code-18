#定义一个递归函数，处理嵌套列表数据
def print_lol(movie):
	for items in movie:
		if isinstance(items,list):
			print_lol(items)
		else:
			print(items)