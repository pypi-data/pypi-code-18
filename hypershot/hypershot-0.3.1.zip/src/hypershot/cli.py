"""
    Create screen shots of a video file, and upload them to an image host.

    Copyright (c) 2017 Kybernetics Project · MIT licensed

    Usage:
        hypershot [options] upload <image>...
        hypershot [options] services
        hypershot [options] templates
        hypershot [options] <video>...
        hypershot (-h | --help)
        hypershot --version

    Options:
        -h, --help          Show this screen.
        --version           Show version.
        --debug             Enable debugging features?
        -q, --quiet         Hide result output?
        -v, --verbose       Verbose logging?
        -n, --dry-run       Do not really upload images
        -P, --no-progress   No progress display

        -c PATH, --config-dir=PATH
            Custom configuration directory.

        -s NAME, --service=NAME
            Select image hosting service.

        -t NAME, --template=NAME
            Select template for result formatting.

        -T PIXELS, --thumb-size=PIXELS
            Also create thumbnail with given width.
"""
import os
import re
import sys
import json
import textwrap

import colorama.ansi
from addict import Dict as attrdict
from docopt import docopt

from . import config, util, handlers, templating
from . import __name__ as appname, __version__


def parse_args():
    """Return command line options and arguments."""
    location = os.path.commonprefix([__file__, os.path.realpath(sys.argv[0]), sys.prefix])
    location = util.pretty_path(location)
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
        elif key.startswith('-'):  # pragma: no-cover
            options[name[1:]] = val
        elif key.startswith('<') and key.endswith('>'):
            args[name[1:-1]] = val
        elif key.isalnum():
            args[name] = val
        else:  # pragma: no-cover
            raise ValueError('Internal error: Invalid docopt key "{}"'.format(key))

    return attrdict(options), attrdict(args)


def image_service():
    """Return handler for selected image service."""
    service_name = config.service or 'imgur'
    if service_name not in config.services:
        util.fatal("No service configuration entry for '{}'".format(service_name))

    settings = attrdict(config.services[service_name])
    if 'handler' not in settings:
        util.fatal("You MUST provide a handler for image service '{}'".format(service_name))

    try:
        handler_class = handlers.REGISTRY[settings.handler]
    except KeyError:
        util.fatal("Unknown handler name '{}' used in service '{}'".format(settings.handler, service_name))

    return handler_class(settings)

class HyperShot():
    """The command line interface."""
    # FG/BG: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # and    LIGHTBLACK_EX, …, LIGHTWHITE_EX
    # Style: RESET_ALL, DIM, NORMAL, BRIGHT, INVERSE
    FG = colorama.Fore
    BG = colorama.Back
    S = util.ExtendedAnsiStyle()

    CONFIG_DEFAULTS = dict(
        services=dict(
            imgur=dict(handler='imgur', login='.netrc'),
        ))

    def __init__(self):
        self.args = None
        self.options = None
        self.table_class = None
        self.namespace = attrdict(settings={}, videos={}, images=[])

    def title(self, text, secondary=False):
        """Return styled title string."""
        return '{}{}››› {} ‹‹‹{}'.format(
            '' if secondary else self.S.BRIGHT,
            self.S.INVERSE, text, self.S.RESET_ALL)

    def results(self, *headers, data=None):
        """Create a terminal table object to display results."""
        table = self.table_class([[
            self.S.BRIGHT + re.sub('^[<=>]', '', x) + self.S.RESET_ALL
            for x in headers]])

        justify = {'<': 'left', '=': 'center', '>': 'right'}
        for idx, header in enumerate(headers):
            table.justify_columns[idx] = justify.get(header[0], 'left')

        if data:
            table.table_data.extend(data)

        return table

    def upload(self):
        """The 'upload' sub-command."""
        # Check template existence, fail early if not found
        templating.load(config.template)

        handler = image_service()
        self.namespace.settings = handler.settings

        # Check given images, fail early on problems
        for image in self.args.image:
            handler.validate(image)

        # Upload all images
        for image in self.args.image:
            webimg = handler.upload(image)
            self.namespace.images.append(webimg)
            if config.progress:
                print("{} → {}".format(image, webimg.hypershot.link))

        # Render results
        result = templating.render(config.template, self.namespace.to_dict())
        if not config.quiet:
            print(result.rstrip())

        # TODO: paste to clipboard

    def services(self):
        """The 'services' sub-command."""
        # Assemble table data
        data, types_index = [], {}
        for name, settings in sorted(config.services.items()):
            handler = handlers.REGISTRY[settings['handler']](settings)
            if handler.settings.enabled:
                types = ' '.join(sorted(handler.settings.types))
                if types not in types_index:
                    types_index[types] = len(types_index) + 1
                data.append([name, settings['handler'],
                             util.to_bibytes(handler.settings.limit),
                             str(types_index[types]),
                             handler.settings.get('url'),
                            ])

        # Print services table
        results = self.results('Name', 'Handler', '>Max. Size', '>Ext', 'Service URL', data=data)
        print(self.title('Services'))
        print(results.table)

        # Print image types table
        results = self.results('>Ext', 'Image File Extensions',
                               data=sorted(tuple(reversed(x)) for x in types_index.items()))
        print('')
        print(self.title("'Ext'ensions column legend", secondary=True))
        print(results.table)

    def templates(self):
        """The 'templates' sub-command."""
        results = self.results('Name', 'Description',
                               data=sorted(dict(templating.inventory()).items()))
        print(self.title('Templates'))
        print(results.table)

    def video(self):
        """Video file handling."""
        print(self.title('*** Not implemented! ***'))  # TODO

    def main(self):
        """The command line interface."""
        self.options, self.args = parse_args()
        if self.options.debug:
            print("DEBUG docopt:\n    options = {!r}\n    args = {!r}".format(self.options, self.args))

        try:
            util.parse_config(self.options, defaults=self.CONFIG_DEFAULTS)
        except (RuntimeError, EnvironmentError, AssertionError) as cause:
            # have no reliable config yet, so check options
            if self.options.debug:
                raise
            util.fatal(cause)
        if config.debug:
            config.log.debug("Configuration:\n%s",
                             json.dumps(config.items(), indent=4, sort_keys=True))

        try:
            self.table_class = util.TABLE_CLASSES[config.table_style]
        except KeyError:
            util.fatal("Invalid table style '{}'".format(config.table_style))

        try:
            if self.args.upload:
                self.upload()
            elif self.args.services:
                self.services()
            elif self.args.templates:
                self.templates()
            else:
                self.video()
        except (RuntimeError, EnvironmentError, ValueError, AssertionError) as cause:
            util.fatal(cause)


def run():  # pragma: no-cover
    """The CLI entry point."""
    import better_exceptions as dummy

    colorama.init()
    try:
        HyperShot().main()
    except KeyboardInterrupt as cause:
        util.fatal('Aborted by Ctrl-C or termination signal!', cause=cause)
    finally:
        colorama.deinit()
