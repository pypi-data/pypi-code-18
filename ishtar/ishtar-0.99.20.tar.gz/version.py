VERSION = (0, 99, 20)


def get_version():
    return u'.'.join((unicode(num) for num in VERSION))

__version__ = get_version()
