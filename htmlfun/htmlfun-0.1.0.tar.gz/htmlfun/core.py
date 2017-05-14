# -*- coding: utf-8 -*-

# core functions


def el(tag_type, *content):
    """
    Returns a list of strings that represents an HTML element.

    If the first argument passed to *content is a dict, then the dict
    is unpacked into attribute pairs for the element.

    >>> el('div', {'class' : 'navbar'}, "This is my Navbar!")
    ['<div class="navbar">', 'This is my Navbar!', '</div>']

    """
    result = []
    try:  # if content exsists
        if isinstance(content[0], dict):
            attrs_dict, content = content[0], content[1:]
            attrs_pairs = []
            for key in attrs_dict:
                attrs_pairs.append('%s="%s"' % (key, attrs_dict[key]))
            attrs_string = " ".join(attrs_pairs)
            open_tag = "<%s %s>" % (tag_type, attrs_string)
        else:
            open_tag = "<%s>" % tag_type
    except IndexError:  # if content is empty
        open_tag = "<%s>" % tag_type
    close_tag = "</%s>" % tag_type
    result.append(open_tag)
    for item in content:
        result.append(item)
    result.append(close_tag)
    return result


def void_el(tag_type, *content):
    "Same as el but for void elements."
    result = []
    try:  # if content exsists
        if isinstance(content[0], dict):
            attrs_dict, content = content[0], content[1:]
            attrs_pairs = []
            for key in attrs_dict:
                attrs_pairs.append('%s="%s"' % (key, attrs_dict[key]))
            attrs_string = " ".join(attrs_pairs)
            open_tag = "<%s %s>" % (tag_type, attrs_string)
        else:
            open_tag = "<%s>" % tag_type
    except IndexError:  # if content is empty
        open_tag = "<%s>" % tag_type
    result.append(open_tag)
    for item in content:
        result.append(item)
    return result


def flatten(list_of_elements):
    "Returns a generator that flattens a nested list of html elements."
    for tag in list_of_elements:
        if isinstance(tag, str):
            yield tag
        else:
            for nested_tag in flatten(tag):
                yield nested_tag


def build_doc(list_of_tags):
    "Create final doc from list_of_tags."
    wrapped = el("html", list_of_tags)
    return "".join(list(flatten(["<!DOCTYPE HTML>"] + wrapped)))
