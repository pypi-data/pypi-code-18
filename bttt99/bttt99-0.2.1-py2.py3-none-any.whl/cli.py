# -*- coding: utf-8 -*-

import click

from .core import search

@click.command()
@click.argument('moviename')
def main(moviename):
    search(moviename)
     

if __name__ == "__main__":
    main()
