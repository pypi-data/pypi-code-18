"""
This is the "nester.py" module and it provides one function called print_lol()
which prints lists that may or may not include nested lists.
"""
import sys

def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """
    para the_list: type list:  This function  takes a positional argument called "the_list", which is any Python list
        (of-possibly-nested lists). Each data item in the provied list is (recursively)
        printed to the screen on it's own line if the fourth argument 'fh' value is default value'
    para indent: type boolean:  A second argument called "indent" controls whether or not inentations shown on the display.
        This defaults to False: set it to True to switch on.
    para level: type  int:  A third argument called "level"(which defaults to 0) is used to insert tab-stops when a
        nested list is encountered.
    para fh: type filename:  A fourth argument called "fh"(which default to sys.stdout) is used to write data to a disk file
        when fh is not default value. Otherwise print datat to screen.
    return None
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end="", file=fh)
            print(each_item, file=fh)
