"""
Console script for packer
"""

import enum
import typing

import click

import packer.errors
import packer.formatters

class Action(enum.Enum):
    """
    Data transformation action
    """

    MINIMIZE = 'minimize'
    PRETTY = 'pretty'
    VALIDATE = 'validate'

@click.group()
def packer_cli():
    """
    Packer is a simple command line utility for converting data into different
    formats or just changing the formatting of data without changing it to
    a different language.
    """

@packer_cli.command(name='convert')
@click.option(
    '--source', '-s',
    default='-',
    help='The source file to read data from')
@click.argument(
    'input-type',
    type=click.Choice(packer.formatters.Formatter.formatters.keys()))
@click.argument(
    'output-type',
    type=click.Choice(packer.formatters.Formatter.formatters.keys()))
def convert(source: str, input_type: str, output_type: str):
    """
    Converts data from one format to another
    """

    input_formatter_type = packer.formatters.Formatter.get_formatter_class(input_type)
    output_formatter_type = packer.formatters.Formatter.get_formatter_class(output_type)

    with click.open_file(source, 'r') as source_stream:
        try:
            input_formatter = input_formatter_type(source_stream)
        except packer.errors.PackerMalformedDataError:
            click.secho('Malformed data given', err=True, fg='red')
            raise click.Abort()

    output_formatter = output_formatter_type(input_formatter.data)

    click.echo(output_formatter.format_pretty())

def _create_formatter_command(name: str) -> typing.Callable:
    description = f'Formatter for {name} data'

    @packer_cli.command(name=name, help=description)
    @click.option(
        '--action', '-a',
        type=click.Choice([a.value for a in Action]),
        default=Action.PRETTY.value,
        help='The action to perform on the data')
    @click.option(
        '--source', '-s',
        default='-',
        help='The source file to read data from')
    @click.option(
        '--indent', '-i',
        type=int, default=4,
        help='The indent level for pretty formatted data')
    def _command(action: str, source: str, indent: int):
        formatter_type = packer.formatters.Formatter.get_formatter_class(name)

        with click.open_file(source, 'r') as source_stream:
            try:
                formatter = formatter_type(source_stream, indent)
            except packer.errors.PackerMalformedDataError:
                click.secho('Malformed data given', err=True, fg='red')
                raise click.Abort()

        if action == Action.PRETTY.value:
            click.echo(formatter.format_pretty())
        elif action == Action.MINIMIZE.value:
            click.echo(formatter.format_compact())
        elif action == Action.VALIDATE.value:
            click.secho('Data is valid!', fg='green')

    return _command

_create_formatter_command('json')
_create_formatter_command('yaml')

if __name__ == '__main__':
    packer_cli()
