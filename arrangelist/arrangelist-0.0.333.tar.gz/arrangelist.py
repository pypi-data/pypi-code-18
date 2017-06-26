#all_list = ["lo", 271,
#            ["oio",
#             ["9329"]]]
#
def print_arrange(the_list, indent=False, level=0):
    for item_list in the_list:
        if isinstance(item_list, list):
       #     for item in item_list:
             print_arrange(item_list, indent, level+1)
        else:
            if indent:
                for tap_stop in range(level):
                    print ("\t", end='')
            print (item_list)

#print_arrange(all_list, True, 4)
