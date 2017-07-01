#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import subprocess
import importlib

from . import log


def exists(cmd):
    status, result = subprocess.getstatusoutput('whereis %s' % cmd)
    return '/' in result

def run(cmd, cwd='.', prefix='', precmd=[], use_splitter=False):
    log.cmd('%s%s' % (prefix, cmd))
    if use_splitter: log.splitter()

    p = subprocess.Popen('printf \033[90m; ' + ('; '.join(precmd) + ';' if len(precmd) > 0 else '') + cmd, cwd=cwd, shell=True)

    ret = p.communicate()[0]

    print('\033[0m', end='')

    if use_splitter: log.splitter()

    return ret

def get_output_quiet(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').strip()

class Package:
    is_yum = True

    def exists(pkg):
        status, result = subprocess.getstatusoutput('rpm -q %s' % pkg)
        return 'is not install' not in result

    def install(pkg): pass

    def require(yum, apt=None, cmd=None):
        pkg = yum if apt is None or Package.is_yum else apt
        if not (Package.exists(pkg) if cmd is None else Command.exists(cmd)):
            log.doing('Installing linux %r package' % pkg)
            Package.install(pkg)

class Library:
    def exists(lib):
        return importlib.find_loader(lib) is not None

    def install(lib):
        log.doing('Installing python %r package' % lib)
        if Command.exists('sudo'):
            Command.run('sudo pip install %s' % lib, use_splitter=True)
        else:
            Command.run('pip install %s' % lib, use_splitter=True)

    def require(lib):
        if not Library.exists(lib):
            Library.install(lib)
