def print_lol(t_list,index=0,isShow = False):
	if isinstance(t_list,list):
		for item in t_list:
			if isinstance(item,list):
				print_lol(item,index+1,isShow)
	else:
		if isShow:
			for tab_store in range(index):
				print("\t",end="")
		print(t_list)