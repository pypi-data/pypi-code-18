#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os

from qualityplatform.util.file import File_Downloader
from qualityplatform.config import config


def start_macaca_server():
    subprocess.Popen("macaca server --port 4444 --verbose", shell=True)


def run_macaca_test(file_name, case_url):
    File_Downloader.download(config["macaca_dir"] + 'eleme', file_name, case_url)
    os.chdir(config["macaca_dir"])
    subprocess.call('source run.sh eleme/%s' % file_name, shell=True)


def ui_recorder():
    os.chdir(config["macaca_dir"])

    subprocess.Popen('uirecorder --mobile', shell=True)
