#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process
from api.api_server import start_api_server
from handler.agent_task import handle_task
from config import config
import os
import click
import qualityplatform

import logging

APP_DESC = """
     A Terminal Tools For qualityplatform Agent
"""

logger = logging.getLogger(__name__)


def output_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: %s" % qualityplatform.__version__)
    ctx.exit()


@click.command()
@click.option('-v', '--version', is_flag=True, is_eager=True, callback=output_version, expose_value=False)
@click.option('-p', '--path', default=".", type=click.Path(), help='macaca的工作目录')
def parse_command(path):
    config["macaca_dir"] = os.path.join(path)
    check_setting_and_env()
    start_agent_client()


def check_setting_and_env():
    print("checking environment")


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
