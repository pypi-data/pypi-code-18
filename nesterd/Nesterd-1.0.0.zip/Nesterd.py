"""This is a function that defines the printing process of a list"""
"""A list is passed as an argument"""
def print_lol(element):
    """The For loop is used to iterate"""
    for element1 in element:
        """Checking if it contains any nested lists"""
        if isinstance(element1,list):
            """Printing nested lists if present"""
            print_lol(element1)
        else:
            print(element1)
