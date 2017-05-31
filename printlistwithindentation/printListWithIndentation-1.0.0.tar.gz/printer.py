""" This module is designed to print
all the atomic elements in the list.
This is done using learnings from "Head First Python" """

def printer(list_elem,level):
    for each_item in list_elem:
        if(isinstance(each_item,list)):
            printer(each_item,level+1)
        else:
            for each_level in range(level):
                print("\t",end="")
            print(each_item)
            
        
