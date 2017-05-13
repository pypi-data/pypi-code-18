''' This module contains a function prints a list 
and possibly any nested list 
'''


''' This function accepts one positional argument (a list).
It prints the contents of the list and any nested lists.
Each item in the provided list is (recursively) printed
to the screen on it's own line
'''

def print_lol(the_list):
    for each_item in the_list:        
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
        


