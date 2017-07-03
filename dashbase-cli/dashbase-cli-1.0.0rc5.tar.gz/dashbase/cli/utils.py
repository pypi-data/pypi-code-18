from __future__ import unicode_literals

import os
import tarfile

import click

from dashbase.cli.constants import DASHBASE_PROCESS_NAME_PREFIX, DashbaseService
from dashbase.utils.errors import NotFound
from dashbase.utils.processRunner import JavaJarRunner


def echo_without_newline(s):
    return click.echo(s, nl=False)


def get_extensions_path(home_path, exception=False):
    path = os.path.join(home_path, "dashbase-extensions", "target", "lib")
    if os.path.isdir(path):
        return path

    if exception:
        raise NotFound(
            "Dashbase extensions not found! Please check that "
            "`dashbase-extensions` exists in {}.".format(home_path))
    return ""


def find_zk_path(home_path):
    search_dir = os.path.join(home_path, "zookeeper")
    if os.path.exists(search_dir) and os.path.isdir(search_dir):
        return search_dir


def find_extensions_path(home_path):
    search_dir = os.path.join(home_path, "dashbase-extensions", "target", "lib/")
    if os.path.exists(search_dir) and os.path.isdir(search_dir):
        return search_dir


def get_cli_command(cmd, type, name, config_path=None, env_dict=None, port=None,
                    adminport=None, heap_opts=None, partition=None, mirror=None, version=None):
    if type == DashbaseService.MONITOR:
        type = DashbaseService.TABLE

    prefix = "dashbase-cli "

    if cmd == 'stop':
        return "{} {} service {} {}".format(prefix, cmd, type, name)

    if mirror:
        prefix += "--mirror {} ".format(mirror)

    _cmd = '{} {} service {} -p {} -ap {} --heap-opts "{}"'
    cli_cmd = _cmd.format(prefix, cmd, type, port, adminport, heap_opts)
    for key, value in list(env_dict.items()):
        cli_cmd += ' -e "{}={}"'.format(key, value)
    if partition:
        cli_cmd += " -r {}".format(partition)

    if version:
        cli_cmd += " --version {}".format(version)
    cli_cmd += " {} {}".format(name, config_path)
    return cli_cmd


def extract_tar(home, package):
    tar = tarfile.open(os.path.join(home, package))
    tar.extractall(home)
    tar.close()
    os.remove(os.path.join(home, package))


def resolve_cwd(path):
    dirname = os.path.dirname(path)
    return dirname if dirname else os.path.curdir


class DashbaseRunner(JavaJarRunner):
    def __init__(self, jar_file, name, configPath, type):
        JavaJarRunner.__init__(self, jar_file)
        self.name = name
        self.configPath = configPath
        self.type = type
        self.add_system_env("processname", "{}-{}-{}".format(DASHBASE_PROCESS_NAME_PREFIX, type, name))
        self.add_system_env("configPath", configPath)

    def add_env(self, key, value):
        JavaJarRunner.add_env(self, {unicode(key): unicode(value)})

    def add_port(self, port, adminPort=None):
        if port:
            self.add_env("PORT", port)
            self.add_system_env("dashbase.port", port)
        if adminPort:
            self.add_env("ADMINPORT", adminPort)
            self.add_system_env("dashbase.adminport", adminPort)

    def add_https_port(self, https_port, https_adminPort=None):
        if https_port:
            self.add_env("HTTPS_PORT", https_port)
        if https_adminPort:
            self.add_env("HTTPS_ADMINPORT", https_adminPort)

    def add_partition(self, partition):
        self.add_env("PARTITION", partition)
        self.add_system_env("dashbase.partition", partition)

    def add_heap_opt(self, opts):
        for opt in opts.split():
            self.add_arg(opt)

    def add_extensions(self, path):
        self.add_system_env("dashbase.ext.dir", path)

    def build_cmd(self):
        c = JavaJarRunner.build_cmd(self)
        c.append("server")
        c.append(os.path.abspath(self.configPath))
        return c
