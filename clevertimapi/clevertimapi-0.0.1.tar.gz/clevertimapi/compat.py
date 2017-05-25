
try:
    basestring
    string_types = (basestring,)
except NameError:
    string_types = (str, bytes)
