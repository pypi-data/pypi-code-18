"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m check_pypi_name_cli` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``check_pypi_name_cli.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``check_pypi_name_cli.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import re

import check_pypi_name
import click


@click.command()
@click.argument('package_name', nargs=1)
def main(package_name):
    normalized_package_name = re.sub(r"[-_.]+", "-", package_name).lower()
    click.echo('Normalised package name: ', nl=False)
    click.echo(normalized_package_name, nl=False)
    click.echo(' is ', nl=False)
    results = check_pypi_name.check_pypi_name(normalized_package_name)
    if results:
        click.echo('Not Available', color='red')
    else:
        click.echo('Available', color='green')
