'''一个函数，用来进行复杂数据列表的重复提取'''
#用了递归的技术

def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            
            print(each_item)

'''
def print_lol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_steps in range(level):
                print('\t',end='')
            print(each_item)
'''
