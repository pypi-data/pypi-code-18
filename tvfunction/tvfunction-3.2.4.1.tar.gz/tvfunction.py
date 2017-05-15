def tv_list(the_list,indent=False,level=0):
    for each_tv in the_list:
        if isinstance(each_tv,list):
            tv_list(each_tv,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='')
            print(each_tv)
            
