def showList(_list):
	for item in _list:
		if(isinstance(item,list)):
			showList(item)
		else:
			print(item)
		
