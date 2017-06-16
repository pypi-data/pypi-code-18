def print_loop(the_list):
	for each_one in the_list:
		if isinstance(each_one,list):
			print_loop(each_one)
		else:
			print(each_one)
