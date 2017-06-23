"""this is  a function about show list"""
def print_lol (the_list,level):
	"""this is  a function about show list"""
	for each_item in the_list:
		if isinstance (each_item,list):
			print_lol(each_item,level)
		else:
            for tab_stop in range(level+1):
                print("\t",end='')
			print(each_item)

