"""this is nester.py module and it provides one function called print_movies which prints lists that may or maynot include nested lists"""
def print_movies(the_list, level):
        #print_movies function is recursive function to print all nested lists items
        for items in the_list:
            if isinstance(items,list):
                print_movies(items,level+1)
            else:
                for tab_stop in range(level):
                    print("\t")
                print(items)
