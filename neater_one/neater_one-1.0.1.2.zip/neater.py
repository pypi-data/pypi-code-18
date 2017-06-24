"""this is  a function about show list"""
def print_lol (the_list,level=0):
    """this is  a function about show list"""
    for each_item in the_list:
        if isinstance (each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)

name = ['John','Eric',['Cleese','Idle'],'Michael',['Palin']]

print_lol(name,0)