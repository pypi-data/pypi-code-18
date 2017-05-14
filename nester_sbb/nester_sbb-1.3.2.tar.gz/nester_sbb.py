"""This is the standard way to 
include a muliple-line comment in
your code."""
import sys

def print_lol(the_list, indent=False, level=0, out=sys.stdout):
        """This function defined a recursive way
	to print a nested list var加个中文"""
        for each_item in the_list:
                if isinstance(each_item, list):
                    print_lol(each_item, indent, level+1, out)
                else:
                    if indent:
                            for i in range(level):
                                    print('\t',end='', file=out)
                    print(each_item, file =out)
