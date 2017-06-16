""" Hypershot Utilities.
"""
import io
import os
import sys
import json
import logging.config

import yaml
import appdirs
import colorama
import terminaltables

from . import config


class SmartJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles sets."""

    def default(self, o):  # pylint: disable=method-hidden
        try:
            iterable = iter(o)
        except TypeError:
            return super().default(o)
        else:
            return list(iterable)


class ExtendedAnsiStyle(colorama.ansi.AnsiCodes):
    """Additional styles compared to ``colorama.Style``."""
    RESET_ALL = 0
    BRIGHT = 1
    DIM = 2
    INVERSE = 7
    NORMAL = 22


class BareTable(terminaltables.AsciiTable):
    """No borders."""

    def __init__(self, table_data, title=None):
        super().__init__(table_data, title)
        self.padding_left = 0
        self.padding_right = 2
        self.outer_border = False
        self.inner_column_border = False
        self.inner_heading_row_border = False

TABLE_CLASSES = dict(
    bare=BareTable,
    ascii=terminaltables.AsciiTable,
    single=terminaltables.SingleTable,
    double=terminaltables.DoubleTable,
)


def pretty_path(path):
    """Return prettyfied filesystem path."""
    path = (path + os.sep).replace(os.path.expanduser('~' + os.sep), '~' + os.sep)
    return path.rstrip(os.sep)


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
        # TO DO: elif isinstance(default_val, list):
        # TO DO: elif isinstance(default_val, dict):
    except (TypeError, ValueError) as cause:
        raise ValueError('Bad value "{val}" for key "{key}": {cause}'
                         .format(key=key, val=val, cause=cause)) from None

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


def fatal(message, cause=None):
    """Exit with a fatal error message."""
    if isinstance(message, Exception):
        cause = cause or message
        message = str(message)
    if cause and config.debug:
        raise cause  # pylint: disable=raising-bad-type
    print(colorama.Style.BRIGHT + colorama.Fore.WHITE + colorama.Back.RED +
          "FATAL:" + colorama.Style.RESET_ALL + ' ' + message)
    sys.exit(1)


def logging_level(settings):
    """Set root logger level."""
    logging.getLogger().setLevel(logging.DEBUG if settings.debug else
                                 logging.INFO if settings.verbose else
                                 logging.WARNING)


def logging_setup(settings, config_dir, appname=None):
    """Initialize logging."""
    from . import __name__ as default_appname

    for ext in ('.yaml', '.yml', '.ini'):
        logging_cfg = os.path.join(config_dir, 'logging' + ext)
        if os.path.exists(logging_cfg):
            break
    else:
        logging_cfg = None

    if not logging_cfg:
        logging.basicConfig()
    elif logging_cfg.endswith('.ini'):
        logging.HERE = config_dir
        logging.config.fileConfig(logging_cfg)
    else:
        with io.open(logging_cfg, encoding='utf-8') as cfg_handle:
            try:
                config_dict = parse_yaml(cfg_handle)
            except yaml.YAMLError as cause:
                raise RuntimeError("Cannot parse YAML file '{}': {}".format(logging_cfg, cause)) from cause
        logging.config.dictConfig(config_dict)
        if settings.debug:
            config.log.debug('Logging config is:\n%s',
                             json.dumps(config_dict, indent=4, sort_keys=True))

    logging_level(settings)
    config.log = logging.getLogger(appname or default_appname)
    if logging_cfg:
        config.log.debug('Logging config read from "%s"', logging_cfg)


def parse_config(options, defaults=None, appname=None, init_logging=True):
    """ Populate 'config' module from configuration file, the environment, and CLI options.

        ``defaults`` can provide additonal configuration defaults, which are merged
        into the YAML hierarchy (scalar values, and the values in top-level dicts).
    """
    from . import __name__ as default_appname, __version__, section

    # Read a config file, if found
    config_dir = appdirs.user_config_dir(appname or default_appname, section)
    config_dir = os.environ.get((appname or default_appname).upper() + '_CONFIG_DIR', config_dir)
    config_dir = options.config_dir or config_dir
    if init_logging:
        logging_setup(options, config_dir, appname)
    config.log.debug("Configdir: %s", config_dir)
    config.config_dir = config_dir

    config_vals = {}
    for ext in ('.yaml', '.yml'):
        cfg_file = os.path.join(config_dir, 'config' + ext)
        if os.path.exists(cfg_file):
            with io.open(cfg_file, encoding='utf-8') as cfg_handle:
                try:
                    config_vals = parse_yaml(cfg_handle)
                except yaml.YAMLError as cause:
                    raise RuntimeError("Cannot parse YAML file '{}': {}".format(cfg_file, cause)) from cause
            break
    for key, val in (defaults or {}).items():
        if isinstance(val, dict):
            config_vals.setdefault(key, {})
            for key2, val2 in val.items():
                config_vals[key].setdefault(key2, val2)
        else:
            config_vals.setdefault(key, val)
    config.log.debug("YAML Config:\n%s", json.dumps(config_vals, indent=4, sort_keys=True))

    # Override config defaults from command line, environment, or config file
    for key, default_val in vars(config).items():
        if key.startswith('_'):
            continue

        val, scope = None, ''
        env_key = ('{}_{}'.format(appname or default_appname, key)).upper()
        if options.get(key) not in (None, False):
            val, scope = options[key], 'cli::'
        elif env_key in os.environ:
            val, scope = os.environ[env_key], 'env::'
        elif key in config_vals:
            val, scope = config_vals[key], 'cfg::'

        if val is not None:
            try:
                setattr(config, key, coerce_to_default_type(scope + key, val, default_val))
                if key.startswith('no_'):
                    # prevent double negatives in application code
                    setattr(config, key[3:], not getattr(config, key))
            except ValueError as cause:
                raise RuntimeError("Invalid config value: {}".format(cause)) from cause

    # Post processing
    logging_level(config)
    if options.verbose and not options.no_progress:
        config.no_progress, config.progress = False, True
