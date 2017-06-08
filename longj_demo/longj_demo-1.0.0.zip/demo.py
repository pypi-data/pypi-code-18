def print_lol(t_list):
	if isinstance(t_list,list):
		for item in t_list:
			if isinstance(item,list):
				print_lol(item)
	else:
		print(t_list)