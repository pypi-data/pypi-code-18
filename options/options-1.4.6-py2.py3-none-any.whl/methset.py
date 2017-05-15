import sys

"""
Support functions for method- and function-specific
setting.
"""

# FIXME: Currenlty depends on class-level meth_defaults dict
# which doesnt apply to functions, and is coarse. Switch instead
# to __kwargs__

_PY3 = sys.version_info[0] > 2

def method_push(base_options, kwdefaults, kwargs):
    """
    Transitional helper function to simplify the grabbing of
    method-specific arguments. Evolved from first-gen approach.
    Still evolving.
    """
    mkwargs = kwdefaults.copy()
    mkwargs.update(kwargs)
    if base_options:
        answer = base_options.push(mkwargs)
        answer.update(mkwargs) # add everything else, for subclasses
                               # probably needs to be a pushall option for this use case
        return answer
    else:
        return mkwargs


def enable_func_set(entry, cls=None):
    """
    :param entry: The method or function to be made settable.
    :para cls: Optional class. Required if target is a method or method name.
    """
    if cls is None:
        raise NotImplementedError
    func = entry if _PY3 else entry.__func__
    if (not hasattr(func, '__kwdefaults__') or
        func.__kwdefaults__ is None):
        func.__kwdefaults__ = {}
    setattr(func, 'set', lambda **kwargs: func.__kwdefaults__.update(kwargs))
