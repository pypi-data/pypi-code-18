"""This is the “nester.py" module, and it provides one function called print_lol() Which prints lists that may or may not include nested lists."""
import sys
"""teste andrey"""

def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
    for item in the_list:
        if isinstance(item, list):
            print_lol(item, indent, level+1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fh)
            print(item, file=fh)