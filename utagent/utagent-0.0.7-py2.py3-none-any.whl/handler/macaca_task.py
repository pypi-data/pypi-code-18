#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os

from qualityplatform.util.file import File_Downloader
import qualityplatform.config as config


def start_macaca_server():
    subprocess.Popen("macaca server --port 4444 --verbose", shell=True)


def run_macaca_test(file_name, case_url):
    File_Downloader.download(config.WORK_SPACE + 'eleme', file_name, case_url)
    os.chdir(config.WORK_SPACE)
    subprocess.call('source run.sh eleme/%s' % file_name, shell=True)


def ui_recorder():
    os.chdir(config.WORK_SPACE)

    subprocess.Popen('uirecorder --mobile', shell=True)
