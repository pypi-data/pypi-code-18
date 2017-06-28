#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process
from api.api_server import start_api_server
from handler.agent_task import handle_task
from config import (
    config,
    environment
)
import os
import click
import slave

import logging

APP_DESC = """
     A Terminal Tools For slave Agent
"""

logger = logging.getLogger(__name__)


def output_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: %s" % slave.__version__)
    ctx.exit()


@click.command()
@click.option('-v', '--version', is_flag=True, is_eager=True, callback=output_version, expose_value=False)
@click.option('-e', '--env', default="alpha", help='The environment of server')
@click.option('-p', '--path', default=".", type=click.Path(), help='The path of uirecorder workspace')
def parse_command(path, env):
    config["macaca_dir"] = os.path.join(path)
    config["environment"] = environment[env]
    start_agent_client()


def start_agent_client():
    p1 = Process(target=start_api_server)
    p2 = Process(target=handle_task)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def main():
    print(APP_DESC)
    parse_command()


if __name__ == "__main__":
    main()
