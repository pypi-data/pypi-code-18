import os
from .util import run

def MHFolder(x):
    if isinstance(x, str) and x[:1] in {'@', '+'}:
        return x
    else:
        raise ValueError('Not an MH folder: %s' % repr(x))

def MHFile(x):
    if isinstance(x, str) and '/' not in x:
        path = run('mhparam', 'path').strip()
        full = os.path.join(os.environ['HOME'], path, x)
        if os.path.isfile(full):
            return full
        else:
            raise ValueError('No such file: %s' % full)
    else:
        raise ValueError('Must not contain slashes: %s' % repr(x))

