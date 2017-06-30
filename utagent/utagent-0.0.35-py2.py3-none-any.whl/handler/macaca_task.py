#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
import webbrowser

from slave.util.file import File_Downloader
from slave.config import config


def start_macaca_server():
    subprocess.Popen("macaca server --port 4444 --verbose", shell=True)


def run_macaca_test(file_name, case_url):
    File_Downloader.download(config["macaca_dir"] + '/eleme', file_name, case_url)
    os.chdir(config["macaca_dir"])
    subprocess.call('source run.sh eleme/%s' % file_name, shell=True)


def ui_recorder():
    os.chdir(config["macaca_dir"])

    subprocess.Popen('uirecorder --mobile', shell=True)


def init_uirecorder():
    os.chdir(config["macaca_dir"])
    import pexpect

    child = pexpect.spawn('uirecorder init --mobile -l en')
    child.expect('ip')
    child.sendline('127.0.0.1')
    child.expect('port')
    child.sendline('4444')

    # subprocess.Popen('uirecorder init --mobile', shell=True)


def reports():
    webbrowser.open_new(config["macaca_dir"]+"/reports/index.html")
