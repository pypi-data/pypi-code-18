'''定义一个函数，用来输出列表中的值，并判断它是否存在列表嵌套，
针对存在列表嵌套的列表进行缩进控制'''
def mov_pr(oldlist,indent=False,leavel=0):
	for mylist in oldlist:
		if isinstance(mylist,list):
			mov_pr(mylist,indent,leavel+1)
		else:
			"""inden=True 的时候进行缩进处理"""
			if indent:
				print('\t'*leavel,end='')
			print(mylist)
