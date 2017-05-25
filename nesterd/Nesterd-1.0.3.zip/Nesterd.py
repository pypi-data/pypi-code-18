"""This is a function that defines the printing process of a list"""
"""A list is passed as an argument"""
def print_lol(element,option=False,indent=0):
    """The For loop is used to iterate"""
    for element1 in element:
        """Checking if it contains any nested lists"""
        if isinstance(element1,list):
            """Printing nested lists if present"""
            if option==False:
                print_lol(element1)
            else:    
                print_lol(element1,True,indent+1)
        else:
            for i in range(indent):
                print("\t",end='') 
            print(element1)
