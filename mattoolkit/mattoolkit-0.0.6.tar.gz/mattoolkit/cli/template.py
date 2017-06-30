# coding: utf-8

import click

from . import cli
from ..template import parse_yaml_files


@cli.command()
@click.option('-r', '--recursive', is_flag=True)
@click.option('-t', '--test', is_flag=True)
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
def create(recursive, test, paths):
  print('Create command')
  print('recursive: ', recursive, 'test: ', test, 'paths: ', paths)
  representations = parse_yaml_files(paths, recursive, test)

  print('Documents in resolved order:')
  for representation in representations:
    print(representation)


# @cli.command()
# @click.option('-r', '--recursive', is_flag=True)
# @click.option('-t', '--test', is_flag=True)
# @click.argument('files', type=click.Path(exists=True), nargs=-1)
# def delete(recursive, test, files):
#   print('Delete command')
#   print(recursive)
#   print(test)
#   print(files)
