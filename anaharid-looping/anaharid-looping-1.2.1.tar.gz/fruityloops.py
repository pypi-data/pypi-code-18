""" Yet another loop to loop internall any list structures 
and print items line"""

def print_all(mylist,indent=False,level=0):
	""" Print method to recurse over or recursiely call"""
	for each in mylist:
		if isinstance(each,list):
			print_all(each,indent,level+1);
		else:
			if indent:
				for i in range(level):
					print("\t",end='')
			print(each);


