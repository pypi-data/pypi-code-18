"""this model for python just a example of my study,
so don't take it consideration."""

def print_plus(the_list):

	"""this function is just print all the item of a list including inner list"""

	for item in the_list:
		if isinstance(item,list):
			print_plus(item);
		else:
			print(item);

