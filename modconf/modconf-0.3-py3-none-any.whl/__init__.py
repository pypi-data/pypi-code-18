__version__ = '0.3'

import sys

def import_conf(name, folder=None):
    sys.path.insert(0, folder)
    
    try:
        m = __import__(name, fromlist='*')
    except:
        print('modconf folder={}'.format(repr(folder)))
        raise
    finally:
        sys.path.pop(0)

    return m

def import_class(mod_name, class_name, args, folder=None):
    mod = import_conf(mod_name, folder)
    cls = mod.__dict__[class_name]
    cls.prepare(*args)
    return cls



