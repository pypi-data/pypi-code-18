# this file duplicates lazyprop many times because i can't work out how to
# automatically add the right docstring...

def lazyprop(fn):
    """Lazy loading class attributes, with hard-coded docstrings for now..."""
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        """A list-like object containing a corpus' subcorpora.

        :Example:

        >>> corpus.subcorpora
        <corpkit.corpus.Datalist instance: 12 items>

        """
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop


class lazy_property(object):
    '''
    meant to be used for lazy evaluation of an object attribute.
    property should represent non-mutable data, as it replaces itself.
    '''

    def __init__(self,fget):
        self.fget = fget
        self.func_name = fget.__name__


    def __get__(self,obj,cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj,self.func_name,value)
        return value