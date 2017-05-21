#定义一个递归函数，处理嵌套列表数据
def print_lol(movie,level):
	for items in movie:
		if isinstance(items,list):
			print_lol(items,level+1)
		else:
			for num in range(level):
				print("\t",end='')
			print(items)