import sys
def print_lol(the_list,indent=False,level1=0,fh=sys.stdout):
    for each_line in the_list:
        if isinstance(each_line,list):
            print_lol(each_line,indent,level1+1,fh)
        else:
            if indent:
                for tab_stop in range(level1):
                    print("\t",end='',file=fh)
            print(each_line,file=fh)

