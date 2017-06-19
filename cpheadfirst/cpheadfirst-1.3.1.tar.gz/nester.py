'''This is the nester.py module and it provides one function print_lol() which print lists
that may or may not include nested lists'''
def print_lol(the_list, indent=False,level=0):
	for each_item in the_list:
		if isinstance(each_item, indent, list):
			print_lol(each_item, level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
			print(each_item)