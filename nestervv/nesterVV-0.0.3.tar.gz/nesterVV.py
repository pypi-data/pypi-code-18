"""This is a fucntion that can print nested list"""
"""This fucntion need one values as its variable"""
"""level means when print recursive list, the list will be print with tabs"""
movies=["The holy grail",1975,"Terrys",91,["Graham",["Mike","John","Eric"]]]
def print_lol(the_list,indent=False,level=0):
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,indent,level+1)
        else:
                if indent:
                    for num in range(level):
                        print("\t",end='')
                print(item)
