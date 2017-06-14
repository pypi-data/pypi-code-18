""" Hypershot Utilities.
"""
import sys


def fatal(message):
    """Exit with a fatal error message."""
    print("FATAL: " + message)  # TODO: use logging
    sys.exit(1)


def bibytes(size):
    """ Convert string ending with an optional unit character (K, M, G) to byte size.
    """
    if isinstance(size, int):
        return size
    if isinstance(size, float):
        return int(size)

    units = "BKMGT"
    scale = 1
    size = size.upper()
    if any(size.endswith(x) for x in units):
        scale = 1024**units.index(size[-1])
        size = size[:-1]

    return int(float(size) * scale)


def to_bibytes(size):
    """ Return an IEC 'bibytes' representation of a byte size.

        See https://en.wikipedia.org/wiki/Binary_prefix.
    """
    if isinstance(size, str):
        size = int(size, 10)
    if size < 0:
        raise ValueError("Negative byte size: {}".format(size))

    if size < 1024:
        return "{:4d} bytes".format(size)
    for unit in ("Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi", "Yi"):
        size /= 1024.0
        if size < 1024:
            return "{:6.1f} {}B".format(size, unit)

    raise ValueError("Insane byte size: {:.1f} YiB".format(size))


def coerce_to_default_type(key, val, default_val):
    """Coerce a given string to the type of a default value."""
    if not isinstance(val, str):
        return val

    newval = val
    try:
        if isinstance(default_val, bool):
            newval = val.lower() in ('1', 'true', 'on', 'enable', 'enabled')
            if newval is False and val.lower() not in ('0', 'false', 'off', 'disable', 'disabled'):
                raise ValueError("Expecting a true/false value")
        elif isinstance(default_val, int):
            newval = int(val)
        # TODO: elif isinstance(default_val, list):
        # TODO: elif isinstance(default_val, dict):
    except (TypeError, ValueError) as cause:
        raise ValueError('Bad value "{val}" for key "{key}": {cause}'.format(
                         key=key, val=val, cause=cause)) from None

    return newval


def parse_yaml(stream):
    """ Safely parse a YAML stream.

        Parse the first YAML document in the given stream
        and produce the corresponding Python object.

        Also see https://github.com/anthonywritescode/episodes-wat/blob/master/02-pyyaml/slides.md
    """
    from yaml import load
    try:
        from yaml.cyaml import CSafeLoader as SafeYamlLoader
    except ImportError:
        from yaml import SafeLoader as SafeYamlLoader

    return load(stream, Loader=SafeYamlLoader)
