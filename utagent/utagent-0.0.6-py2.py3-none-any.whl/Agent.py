#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process
from api.api_server import start_api_server
from handler.agent_task import handle_task
from config import config
import os
import click

import logging

APP_DESC = """
     A Terminal Tools For qualityplatform Agent
"""

logger = logging.getLogger(__name__)


@click.command()
@click.option('-p', '--path', default=".", type=click.Path(), help='视频缓存本地地址,注:quality必须要为1-2-3其中之一')
@click.option('-v', '--verbose', count=True, help='-v 为普通日志模式, -vvvv 超级海量日志模式')
def parse_command(path, verbose):
    current_working_dir = os.getcwd()
    config["macaca_dir"] = os.path.join(path)
    config["verbose"] = verbose
    logger.info("正在检查环境")
    check_setting_and_env()
    logger.info("环境检查完毕,正在开启Agent(请等待15s~30s)")
    start_agent_client()


def check_setting_and_env():
    logger.info("程序正在启动,检查环境配置")
    logger.info("开始配置环境")


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
