import os
import subprocess

import click
import psutil

from dashbase.cli.cli import pass_context, root
from dashbase.cli.constants import DASHBASE_PROCESS_PREFIX, list_services, ZOOKEEPER
from dashbase.cli.parameters import NAME
from dashbase.cli.utils import get_cli_command, echo_without_newline
from dashbase.services import LogService
from dashbase.utils.configParser import ClusterConfigParser
from dashbase.utils.errors import CliRuntimeError
from dashbase.utils.ssh import Connect


@root.group()
@pass_context
def cmd_stop(ctx):
    """Stop a running Dashbase services or ZooKeeper."""
    pass


@cmd_stop.command(ZOOKEEPER, help='Stop running ZooKeeper.')
@pass_context
def cmd_stop_zookeeper(ctx):
    """Stop a running ZooKeeper"""
    home = ctx.config.get("home", "")
    zookeeper_path = "{}/zookeeper/".format(home)
    if not os.path.exists(zookeeper_path):
        raise CliRuntimeError("ZooKeeper not found in {}, try running "
                              "`dashbase install zookeeper` first.".format(home))
    os.chdir(zookeeper_path)
    cmd = "./bin/zkServer.sh stop"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    click.secho(p.communicate()[0])


@cmd_stop.command('service', short_help='Stop a running Dashbase service.')
@click.argument('type', nargs=1, type=click.Choice(list_services()))
@click.argument('name', nargs=1, type=NAME)
@pass_context
def cmd_stop_service(ctx, type, name):
    """Stop a running Dashbase service."""
    for proc in psutil.process_iter():
        try:

            if proc.name() == "java" and DASHBASE_PROCESS_PREFIX in " ".join(proc.cmdline()):
                cmd = proc.cmdline()
                process_type = cmd[1].split("-")[2]
                process_name = "-".join(cmd[1].split("-")[3:])
                if name == process_name and type == process_type:
                    proc.kill()
                    click.secho("Successfully stopped dashbase-{}: {}".format(type, name))
                    return

        except psutil.NoSuchProcess:
            pass

    raise CliRuntimeError("""Can't find dashbase-{}: {}
Please check the service name or user permissions.""".format(type, name))


@cmd_stop.group()
@click.option('--config',
              type=click.Path(exists=True, file_okay=True, dir_okay=False,
                              resolve_path=True),
              help='Custom dashbase.yml configuration.')
@pass_context
def cluster(ctx, config):
    """Stop a running Dashbase cluster."""
    if config:
        ctx.app_config = ClusterConfigParser(src=config)
    if not ctx.app_config:
        raise CliRuntimeError("Cluster requires a `dashbase.yml`."
                              "This file is in the CLI config home path by "
                              "default or can be specified by "
                              "`dashbase stop cluster --config PATH`")
    pass


@cluster.command('all', short_help="Stop all services for a Dashbase cluster.")
@pass_context
def cmd_stop_cluster_all(ctx):
    ctx.app_config.parse()
    services = ctx.app_config.services
    hosts = ctx.app_config.hosts
    for key, service_objects in list(services.items()):
        service = service_objects.get()
        type = service['type']
        conf_host = service['host']
        if conf_host not in hosts:
            raise CliRuntimeError("`host` for service {} does not have a matching host configuration.".format(key))
        host = hosts[conf_host].get()

        cli_cmd = get_cli_command('stop', type, key)
        click.secho("\nStopping {} on {}".format(key, host['hostname']))
        with Connect(host['hostname'], host['username'], private_file=host['private_key']) as ssh:
            ret, output = ssh.run(cli_cmd, echo_without_newline)
            if ret != 0:
                LogService.log('Using command: {}'.format(cli_cmd), show=False)
                LogService.log('Output is:', show=False)
                LogService.log(output, show=False, nl=False)
