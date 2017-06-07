def listAll(newList,level=0):
	for eachItem in newList:
		if isinstance(eachItem,list):
			listAll(eachItem,level+1)
		else :
			for i in range(level):
				print ("\t",end='')
			print (eachItem)
