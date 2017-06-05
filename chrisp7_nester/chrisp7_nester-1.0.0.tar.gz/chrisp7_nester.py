def listAll(newList):
	for eachItem in newList:
		if isinstance(eachItem,list):
			listAll(eachItem)
		else :
			print (eachItem)
