"""
A thin wrapper around [hjson](http://github.com/hjson/hjson-py).

>>> from hjs import hjs, dumps, loads, dump, load
>>> da = hjs('''
... {
...    a: 1
...    b: are you ok with it ?
...    t: {
...        a: you get the point, now :-)
...    },
...    values: 42
... }
... ''')
>>> assert da['values'] == 42
>>> assert da.t.a == "you get the point, now :-)"
"""
from collections import OrderedDict
import hjson


from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'X.X.X'

del get_distribution, DistributionNotFound

try:
    unicode
except NameError:
    basestring = (bytes, str)


class hjs(OrderedDict):
    """
    TODO
    """
    def __init__(self, *args, **kwargs):
        try:
            super(hjs, self).__init__(*args, **kwargs)
        except ValueError:
            if args and isinstance(args[0], basestring):
                super(hjs, self).__init__()
                base = hjson.loads(args[0], object_pairs_hook=self.__class__)
                self.update(base)
                self.update(kwargs)
            else:
                raise

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            self.__setitem__(name, value)

    def __dir__(self):
        return self.keys()

    def __repr__(self):
        return 'hjs("""\n%s""")' % hjson.dumps(self)

    def _repr_pretty_(self, p, cycle):
        p.text(repr(self))


def _wrap(fun):

    from functools import wraps

    @wraps(fun)
    def wrapper(*args, **kwds):
        hook = kwds.get('object_pairs_hook')
        if hook is OrderedDict:
            kwds['object_pairs_hook'] = hjs
        return fun(*args, **kwds)

    return wrapper


loads = _wrap(hjson.loads)  # noqa: F401
load = _wrap(hjson.load)    # noqa: F401
dumps = hjson.dumps         # noqa: F401
dump = hjson.dump           # noqa: F401
