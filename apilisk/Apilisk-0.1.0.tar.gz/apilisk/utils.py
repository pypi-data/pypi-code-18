# Copyright (C) 2014-2015, Availab.io(R) Ltd. All rights reserved.
from jinja2 import Environment
import json


def substitute_variables_recursively(something, variables):
    """
    Recursively substitutes variables in strings, arrays and dictionaries.

    If you try to pass any other object it will be returned unharmed.
    """
    env = Environment()

    if isinstance(something, str) or isinstance(something, unicode):
        return env.from_string(something).render(**variables)
    elif isinstance(something, list):
        new_list = []
        for itm in something:
            new_list.append(substitute_variables_recursively(
                itm, variables)
            )
        return new_list
    elif isinstance(something, dict):
        new_dict = {}
        for key, value in something.iteritems():
            new_key = env.from_string(key).render(**variables)
            new_value = substitute_variables_recursively(value, variables)
            new_dict[new_key] = new_value
        return new_dict
    else:
        return something
