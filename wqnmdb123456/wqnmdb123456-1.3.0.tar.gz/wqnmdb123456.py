def print_lol(the_list,indent=False,level1=0):
    for each_line in the_list:
        if isinstance(each_line,list):
            print_lol(each_line,indent,level1+1)
        else:
            if indent:
                for tab_stop in range(level1):
                    print("\t",end='')
            print(each_line)

