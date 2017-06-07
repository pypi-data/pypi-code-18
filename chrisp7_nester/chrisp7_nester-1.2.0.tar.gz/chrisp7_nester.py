def listAll(newList,doTab=False,level=0):
	for eachItem in newList:
		if isinstance(eachItem,list):
			listAll(eachItem,doTab,level+1)
		else :
			if doTab==True :
				for i in range(level):
					print ("\t",end='')
			print (eachItem)
