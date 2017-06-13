"""
    Create screen shots of a video file, and upload them to an image host.

    Usage:
        hypershot [options] upload <image>...
        hypershot [options] <video>...
        hypershot (-h | --help)
        hypershot --version

    Options:
        -h, --help          Show this screen.
        --version           Show version.
        --debug             Enable debugging features?
        -v, --verbose       Verbose logging?
        -n, --dry-run       Do not really upload images

        -c PATH, --config-dir=PATH
            Custom configuration directory.

        -s NAME, --service=NAME
            Select image hosting service.

        -t PIXELS, --thumb-size=PIXELS
            Also create thumbnail with given width.
"""
import io
import os
import sys
import json
import logging
import textwrap

import appdirs
from addict import Dict as attrdict
from docopt import docopt

from . import config, util, handlers
from . import __name__ as appname, __version__, section


def parse_args():
    """Return command line options and arguments."""
    location = os.path.commonprefix([__file__, os.path.realpath(sys.argv[0]), sys.prefix])
    location = (location + os.sep).replace(os.path.expanduser('~' + os.sep), '~' + os.sep)
    location = location.rstrip(os.sep)
    version_info = '{} {}{}{} using Python {}'.format(
                   appname, __version__,
                   ' from ' if location else '', location,
                   sys.version.split()[0])

    mixed = docopt(textwrap.dedent(__doc__), version=version_info)
    options, args = {}, {}
    for key, val in mixed.items():
        name = key.replace('-', '_')
        if key.startswith('--'):
            options[name[2:]] = val
        elif key.startswith('-'):
            options[name[1:]] = val
        elif key.startswith('<') and key.endswith('>'):
            args[name[1:-1]] = val
        elif key.isalnum():
            args[name] = val
        else:
            raise ValueError('Internal error: Invalid docopt key "{}"'.format(key))

    return attrdict(options), attrdict(args)



def logging_level(settings):
    """Set root logger level."""
    logging.getLogger().setLevel(logging.DEBUG if settings.debug else
                                 logging.INFO if settings.verbose else
                                 logging.WARNING)


def logging_setup(settings, config_dir):
    """Initialize logging."""
    import logging.config

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
                config_dict = util.parse_yaml(cfg_handle)
            except yaml.YAMLError as cause:
                util.fatal("Cannot parse YAML file '{}': {}".format(logging_cfg, cause))
        logging.config.dictConfig(config_dict)
        if settings.debug:
            logging.getLogger(appname).debug('Logging config is:\n%s',
                                             json.dumps(config_dict, indent=4, sort_keys=True))

    logging_level(settings)
    config.log = logging.getLogger(appname)
    if logging_cfg:
        config.log.debug('Logging config read from "%s"', logging_cfg)


def parse_config(options):
    """Populate 'config' module from configuration file, the environment, and CLI options."""
    import yaml

    # Read a config file, if found
    config_dir = appdirs.user_config_dir(appname, section)
    config_dir = os.environ.get('HYPERSHOT_CONFIG_DIR', config_dir)
    config_dir = options.config_dir or config_dir
    logging_setup(options, config_dir)
    config.log.debug("Configdir: %s", config_dir)

    config_vals = {}
    for ext in ('.yaml', '.yml'):
        cfg_file = os.path.join(config_dir, 'config' + ext)
        if os.path.exists(cfg_file):
            with io.open(cfg_file, encoding='utf-8') as cfg_handle:
                try:
                    config_vals = util.parse_yaml(cfg_handle)
                except yaml.YAMLError as cause:
                    util.fatal("Cannot parse YAML file '{}': {}".format(cfg_file, cause))
            break
    config_vals.setdefault('services', {})
    config_vals['services'].setdefault('imgur', dict(handler='imgur', login='.netrc'))
    config_vals['services'].setdefault('default', dict(
        handler='chevereto',
        url='https://malzo.com/',
        limit='25M',
    ))
    config.log.debug("YAML Config:\n%s", json.dumps(config_vals, indent=4, sort_keys=True))

    # Override config defaults from command line, environment, or config file
    for key, default_val in vars(config).items():
        if key.startswith('_'):
            continue

        val, scope = None, ''
        env_key = ('{}_{}'.format(appname, key)).upper()
        if options.get(key) not in (None, False):
            val, scope = options[key], 'cli::'
        elif env_key in os.environ:
            val, scope = os.environ[env_key], 'env::'
        elif key in config_vals:
            val, scope = config_vals[key], 'cfg::'

        if val is not None:
            try:
                setattr(config, key, util.coerce_to_default_type(scope + key, val, default_val))
            except ValueError as cause:
                util.fatal("Invalid config value: {}".format(cause))

    logging_level(config)


def image_service():
    """Return handler for selected image service."""
    image_service = config.service or 'default'
    if image_service not in config.services:
        util.fatal("No service configuration entry for '{}'".format(image_service))

    settings = attrdict(config.services[image_service])
    if 'handler' not in settings:
        util.fatal("You MUST provide a handler for image service '{}'".format(image_service))

    return handlers.REGISTRY[settings.handler](settings)


def run():
    """The CLI entry point."""
    options, args = parse_args()
    if options.debug:
        print("TRACE Options + args:", options, args)

    parse_config(options)
    if config.debug:
        config.log.debug("Configuration:\n%s",
                         json.dumps(config._items(), indent=4, sort_keys=True))

    handler = image_service()

    if args.upload:
        try:
            for image in args.image:
                handler.validate(image)
            for image in args.image:
                webimg = handler.upload(image)
                print(image, '→', webimg.hypershot.link)
            # TODO: put URL list into template engine and paste to clipboard
        except (RuntimeError, ValueError, AssertionError) as cause:
            util.fatal(str(cause))
    else:
        pass
