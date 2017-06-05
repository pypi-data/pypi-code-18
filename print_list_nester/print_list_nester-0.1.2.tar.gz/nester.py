"""This is the 'nester.py' module and it provides a single function called
'print_list()' capable of printing both normal aand nested lists."""
import sys


def print_list(the_list, tab=False, tab_level=0, fh=sys.stdout):
       """Argument 1 - any python list(nested or otherwise)
       Argument 2 - If indentation is wanted (boolean)
       Argument 3 - Amount of indentation in tab space (int)
       Argument 4 - Output location, provide the file name + extension (defaulted to sys display)
       Description - Function will take the given arguments and print all data
       items found in the list and any subsequent lists inside."""
       for each_item in the_list:
              if isinstance(each_item, list):
                     print_list(each_item, tab, tab_level+1, fh)
              else:
                     if tab:
                            for tabs in range(tab_level):
                                   print("\t", end='', file = fh)
                     print(each_item, file = fh)
