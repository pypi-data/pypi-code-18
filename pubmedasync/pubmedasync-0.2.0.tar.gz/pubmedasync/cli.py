# -*- coding: utf-8 -*-

import asyncio

import click

from pubmedasync import test


@click.command()
def main():
    """Console script for pubmedasync"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()


if __name__ == "__main__":
    main()
