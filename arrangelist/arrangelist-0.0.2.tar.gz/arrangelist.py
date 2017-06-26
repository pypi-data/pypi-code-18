#all_list = ["lo", 271,
#            ["oio",
#             ["9329"]]]

def print_arrange(the_list):
    for item_list in the_list:
        if isinstance(item_list, list):
       #     for item in item_list:
             print_arrange(item_list)
        else:
            print (item_list)

#print_arrange(all_list)
