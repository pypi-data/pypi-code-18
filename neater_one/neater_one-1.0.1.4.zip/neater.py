import sys
"""this is  a function about show list"""
def print_lol (the_list,indent=False,level=0,location=sys.stdout):
    """this is  a function about show list"""
    for each_item in the_list:
        if isinstance (each_item,list):
            print_lol(each_item,indent,level+1,location)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='',file=location)
            print(each_item,file=location)