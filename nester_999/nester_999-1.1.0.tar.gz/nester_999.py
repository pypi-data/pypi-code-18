''' This module contains a function prints a list 
and possibly any nested list 
'''


def print_lol(the_list,level):
    ''' This function accepts one positional argument (a list).
    It prints the contents of the list and any nested lists.
    Each item in the provided list is (recursively) printed
    to the screen on it's own line
    indents each item in a nested list by its level
    '''

    for each_item in the_list:        
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print('\t', end='')
            print(each_item)
        


