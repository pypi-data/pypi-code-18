import sys

def import_conf(name, folder=None):
    sys.path.insert(0, folder)

    try:
        m = __import__(name, fromlist='*')
    except:
        print('\n'.join(sys.path))
        raise

    sys.path.pop(0)

    return m

