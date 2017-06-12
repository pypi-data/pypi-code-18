# -*- coding: utf-8 -*-

import click

from roundhouse import __version__
from roundhouse.serializer import get_serializers
from roundhouse.utils import get_file_extension, get_full_qualname


serializers = get_serializers()
serializer_formats = sorted(serializers.keys())
extension_to_format_map = {}

for _ in serializers.values():
    for _ext in _.extensions:
        extension_to_format_map[_ext] = _.format


class ShortChoice(click.Choice):
    """Truncate choices if many options"""

    truncate_after = 3

    def get_metavar(self, param):
        choices = self.choices

        if len(choices) > self.truncate_after:
            choices = choices[:self.truncate_after] + ['...']

        return '[%s]' % '|'.join(choices)


@click.command(context_settings=dict(
    help_option_names=['-h', '--help']
))
@click.version_option(version=__version__)
@click.option(
    '-i',
    '--input-format',
    type=ShortChoice(serializer_formats),
    help='Input format. Inferred from infile extension if not provided'
)
@click.option(
    '-o',
    '--output-format',
    type=ShortChoice(serializer_formats),
    help='Output format. Inferred from outfile extension if not provided'
)
@click.option(
    '-I',
    '--infile',
    type=click.File('rb', lazy=True),
    default='-',
    help='Read from file. Defaults to stdin'
)
@click.option(
    '-O',
    '--outfile',
    type=click.File('wb', lazy=True),
    default='-',
    help='Write to file. Defaults to stdout'
)
@click.option(
    '-p',
    '--pretty',
    is_flag=True,
    help='Prettify output where supported'
)
@click.option(
    '-l',
    '--list',
    'list_',
    is_flag=True,
    help='List all installed available serializers, their formats and extensions, and exit'
)
def main(input_format, output_format, infile, outfile, pretty, list_):
    """Roundhouse

    Convert many formats to many formats
    """

    if list_:
        for serializer_format, serializer_class in sorted(serializers.items()):
            click.echo('\n'.join([
                serializer_format,
                '-' * len(serializer_format),
                'Serializer: ' + get_full_qualname(serializer_class),
                'Format: ' + serializer_format,
                'File Extensions: ' + ', '.join(serializer_class.extensions),
                ''
            ]))

        raise SystemExit

    if input_format is None:
        if infile.name == '-':
            raise click.BadParameter('Must provide input-format when reading from stdin')

        ext = get_file_extension(infile.name)
        input_format = extension_to_format_map.get(ext)
        if input_format is None:
            raise click.BadParameter((
                'Unable to guess serializer format from extension "{}", '
                'check filename or explicitly provide input-format'
            ).format(ext))

    if output_format is None:
        if outfile.name == '-':
            raise click.BadParameter('Must provide output-format when writing to stdout')

        ext = get_file_extension(outfile.name)
        output_format = extension_to_format_map.get(ext)
        if output_format is None:
            raise click.BadParameter((
                'Unable to guess serializer format from extension "{}", '
                'check filename or explicitly provide output-format'
             ).format(ext))

    kwargs = {
        'pretty': pretty
    }

    input_serializer = serializers[input_format](**kwargs)
    output_serializer = serializers[output_format](**kwargs)

    data = input_serializer.deserialize(infile)
    output_serializer.serialize(data, outfile)
