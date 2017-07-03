import os
import subprocess

import click
from pexpect.popen_spawn import PopenSpawn

from dashbase.cli.cli import pass_context, root
from dashbase.cli.cmd.install import download_dashbase
from dashbase.cli.constants import (
    DASHBASE_REMOTE_CONFIG_PATH, DashbaseService, ZOOKEEPER, DASHBASE_EXTENSIONS, DASHBASE_MONITOR_CONFIG, NUM_TRIES,
    DELAY_IN_SECONDS, DASHBASE_CLI_VERSION
)
from dashbase.cli.parameters import NAME, ENV
from dashbase.cli.utils import (
    DashbaseRunner, get_extensions_path, get_cli_command,
    extract_tar, resolve_cwd, echo_without_newline)
from dashbase.services import LogService, JarService, VersionService
from dashbase.utils.adminHealthChecker import DropWizardAdminHealthChecker
from dashbase.utils.configParser import ClusterConfigParser, ServiceConfigParser
from dashbase.utils.errors import CliRuntimeError, NotFound
from dashbase.utils.processManage import get_dashbase_process, get_process_env
from dashbase.utils.ssh import Connect
from dashbase.utils.dependencies import install_dependencies

common_args = [
    click.argument('name', nargs=1, type=NAME),
    click.argument('config', nargs=1, type=click.Path(dir_okay=False))
]

common_options = [
    click.option('--env', '-e', multiple=True, type=ENV),
    click.option('--version', required=False, type=click.STRING)
]


def add_arg_opt(options):
    def _add_arg_opt(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_arg_opt


@root.group()
@pass_context
def cmd_start(ctx):
    """Start a Dashbase services or ZooKeeper."""
    _check_java_version()


@cmd_start.command(ZOOKEEPER, short_help='Start ZooKeeper.')
@pass_context
def cmd_start_zookeeper(ctx):
    home = ctx.config.get("home", "")
    zookeeper_path = "{}/zookeeper/".format(home)
    if not os.path.exists(zookeeper_path):
        raise CliRuntimeError("ZooKeeper not found in {}, try running "
                              "`dashbase install zookeeper` first.".format(home))
    os.chdir(zookeeper_path)
    cmd = "./bin/zkServer.sh start"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env={"ZOO_LOG_DIR": "./../logs/"})
    ret = p.wait()
    stdout, stderr = p.communicate()
    click.secho(stdout)
    if ret:
        # user didn't use sudo so could not write pid
        LogService.log(stderr, fg='red')
        LogService.log('Please try "sudo dashbase start zookeeper".')


@cmd_start.group()
@pass_context
def service(ctx):
    """Start a Dashbase service."""
    pass


@service.command(DashbaseService.TABLE, short_help='Start a Dashbase table partition.')
@pass_context
@add_arg_opt(common_args)
@add_arg_opt(common_options)
@click.option('--port', '-p', default=7888, type=click.INT)
@click.option('--adminport', '-ap', default=7988, type=click.INT)
@click.option('--heap-opts', default="-Xmx4g -Xms2g -XX:NewSize=1g",
              type=click.STRING)
@click.option('--partition', '-r', type=click.INT, default=0)
def cmd_start_table(ctx, name, config, env, port, adminport, heap_opts,
                    partition, version):
    """Start a Dashbase table partition with the given NAME using CONFIG."""
    _start_service(ctx,
                   name=name,
                   service_type=DashbaseService.TABLE,
                   config=config,
                   env=env,
                   port=port,
                   adminport=adminport,
                   heap_opts=heap_opts,
                   partition=partition,
                   version=version)
    return


@service.command(DashbaseService.API,
                 short_help='Start a Dashbase api service.')
@add_arg_opt(common_args)
@add_arg_opt(common_options)
@click.option('--port', '-p', default=9876, type=click.INT)
@click.option('--adminport', '-ap', default=9976, type=click.INT)
@click.option('--heap-opts', default="-Xmx1g -Xms1g -XX:NewSize=512m", type=click.STRING)
@pass_context
def cmd_start_api(ctx, name, config, env, port, adminport, heap_opts, version):
    """Start a Dashbase api service with the given NAME using CONFIG."""
    _start_service(ctx,
                   name=name,
                   service_type=DashbaseService.API,
                   config=config,
                   env=env,
                   port=port,
                   adminport=adminport,
                   heap_opts=heap_opts,
                   version=version)
    return


@service.command(DashbaseService.WEB,
                 short_help='Start a Dashbase web service.')
@add_arg_opt(common_args)
@add_arg_opt(common_options)
@click.option('--port', '-p', default=8080, type=click.INT)
@click.option('--adminport', '-ap', default=8180, type=click.INT)
@click.option('--heap-opts', default="-Xmx1g -Xms1g -XX:NewSize=512m", type=click.STRING)
@pass_context
def cmd_start_web(ctx, name, config, env, port, adminport, heap_opts, version):
    """Start a Dashbase web service with the given NAME using CONFIG."""

    _start_service(ctx,
                   name=name,
                   service_type=DashbaseService.WEB,
                   config=config,
                   env=env,
                   port=port,
                   adminport=adminport,
                   heap_opts=heap_opts,
                   version=version)
    return


@service.command(DashbaseService.AUTH,
                 short_help='Start a Dashbase auth service.')
@add_arg_opt(common_args)
@add_arg_opt(common_options)
@click.option('--port', '-p', default=9898, type=click.INT)
@click.option('--adminport', '-ap', default=9998, type=click.INT)
@click.option('--heap-opts', default="-Xmx1g -Xms1g -XX:NewSize=512m", type=click.STRING)
@pass_context
def cmd_start_auth(ctx, name, config, env, port, adminport, heap_opts, version):
    """Start a Dashbase auth service with the given NAME using CONFIG."""
    _start_service(ctx,
                   name=name,
                   service_type=DashbaseService.AUTH,
                   config=config,
                   env=env,
                   port=port,
                   adminport=adminport,
                   heap_opts=heap_opts,
                   version=version)
    return


@cmd_start.group()
@pass_context
@click.option('--config',
              type=click.Path(exists=True, file_okay=True, dir_okay=False,
                              resolve_path=True),
              default=os.path.join(os.getcwd(), "dashbase.yml"),
              help='Custom dashbase.yml configuration.')
def cluster(ctx, config):
    """Start a Dashbase cluster. Requires a dashbase.yml configuration file."""
    if config:
        ctx.app_config = ClusterConfigParser(src=config)
    if not ctx.app_config:
        raise CliRuntimeError("Cluster requires a `dashbase.yml`."
                              "This file is in the CLI config home path by "
                              "default or can be specified by "
                              "`dashbase start cluster --config PATH`")
    pass


@cluster.command('all', help="Start all services for a Dashbase cluster.")
@pass_context
def cmd_start_cluster_all(ctx):
    ctx.app_config.parse()
    services = ctx.app_config.services
    hosts = ctx.app_config.hosts
    mirror = ctx.app_config.mirror
    version = ctx.app_config.version
    uninstall = ctx.app_config.uninstall
    installed_hosts = []
    for key, service_object in list(services.items()):
        service = service_object.get()
        conf_host = service['host']
        if conf_host not in hosts:
            raise CliRuntimeError("`host` for service {} does not have a matching host configuration.".format(key))
        host = hosts[conf_host].get()
        conf = DASHBASE_REMOTE_CONFIG_PATH + "{}-config.yml".format(key)
        # install CLI on remote machine using `pip install ...`
        install_cmd = "sudo pip install dashbase=={version}".format(version=DASHBASE_CLI_VERSION)
        # uninstall service jars using cli
        uninstall_jar_cmd = 'dashbase uninstall service --all {}'.format(service['type'])
        # start services using cli
        cli_cmd = get_cli_command('start', type=service['type'], name=service['name'], config_path=conf,
                                  env_dict=service['env'], port=service['port'], adminport=service['admin_port'],
                                  heap_opts=service['heap_opts'], partition=service['partition'], mirror=mirror,
                                  version=service['version'])
        click.secho("\nStarting {} on {}".format(key, host['hostname']))
        with Connect(host['hostname'], host['username'], private_file=host['private_key']) as ssh:
            ssh.send_file(service['config'], conf)
            if host['hostname'] not in installed_hosts:
                install_dependencies(ssh)
                ret, output = ssh.run(install_cmd, echo_without_newline)
                if ret != 0:
                    LogService.log('Using command: {}'.format(install_cmd), show=False)
                    LogService.log('Output is:', show=False)
                    LogService.log(output, show=False, nl=False)
                    raise CliRuntimeError('Command failed on remote host.')
                click.echo()
                installed_hosts.append(host['hostname'])
            if uninstall:
                ssh.run(uninstall_jar_cmd, echo_without_newline)
                click.echo()
            ret, output = ssh.run(cli_cmd, echo_without_newline)
            if ret != 0:
                LogService.log('Using command: {}'.format(cli_cmd), show=False)
                LogService.log('Output is:', show=False)
                LogService.log(output, show=False, nl=False)
                raise CliRuntimeError('Command failed on remote host.')


def _start_service(ctx, name, service_type, config, env, port, adminport,
                   heap_opts, version=None, partition=None):
    home = ctx.config.get("home", "")
    type = service_type
    _pre_check(ctx, home, name, service_type, config, version)
    service_config = ServiceConfigParser(config)
    service_config.parse()

    jar = JarService.find_jar_path_by_version(type=type, home_path=home, version=version)
    runner = DashbaseRunner(jar, name=name, configPath=config, type=type)
    cmd = _add_runner_envs(service_config, type, runner, home, env, port, adminport, heap_opts,
                           partition)
    _start_process(cmd, runner, type, config)
    return True


def _pre_check(ctx, home, name, type, config, version, install=True):
    proc = get_dashbase_process(type, name)
    mirror = ctx.config.get('mirror')
    if not version:
        version = VersionService.get_latest_version(mirror)
    if proc:
        raise CliRuntimeError(
            "Dashbase {} service `{}` is already running with pid: {}".format(
                type, name, proc.pid))

    try:
        jar_versions, _ = JarService.get_jar_versions(type=type, home_path=home, exception=True)
    except NotFound:
        jar_versions = []

    if version not in jar_versions:
        if not install:
            raise CliRuntimeError("Can't find dashbase-{}!".format(type))
        VersionService.check_version(mirror=mirror, version=version)
        download_dashbase(type=type, home=home, version=version, mirror=mirror)

    if type == DashbaseService.TABLE or type == DashbaseService.API:
        # verify dashbase-extensions exists, if not, install it
        if not os.path.exists(os.path.join(home, DASHBASE_EXTENSIONS)):
            download_dashbase(type=DASHBASE_EXTENSIONS, home=home, version=version, mirror=mirror)
            extract_tar(home, "{}.tar.gz".format(DASHBASE_EXTENSIONS))

    monitor_config_file = os.path.join(home, "conf", DASHBASE_MONITOR_CONFIG)
    if not os.path.isfile(monitor_config_file):
        from dashbase.cli.cmd.install import download_from_url
        url = "{mirror}/{version}/{monitor_config}".format(mirror=mirror, version=version,
                                                           monitor_config=DASHBASE_MONITOR_CONFIG)
        download_from_url(url, monitor_config_file)

    if not os.path.isfile(config):
        raise CliRuntimeError(
            "`{}` is not a valid config file path.".format(config))
    return True


def _verify_ports(service_config, runner, port, adminport):
    config_port = service_config.get_connector_port(service_config.app_connectors, 'http')
    config_adminport = service_config.get_connector_port(service_config.admin_connectors, 'http')
    if config_port:
        port = config_port
    if config_adminport:
        adminport = config_adminport
    runner.add_port(port, adminport)

    # handle HTTPS, which is not used as often unless for auth
    # if not specified in config.yml, we export defaults as env variables
    https_port = service_config.get_connector_port(service_config.app_connectors, 'https')
    https_adminport = service_config.get_connector_port(service_config.admin_connectors, 'https')
    runner.add_https_port(https_port, https_adminport)


def _add_runner_envs(service_config, type, runner, home, env, port, adminport, heap_opts, partition):
    runner.add_heap_opt(heap_opts)
    _verify_ports(service_config, runner, port, adminport)
    if type == DashbaseService.TABLE or type == DashbaseService.API:
        extensions = get_extensions_path(home, exception=True)
        runner.add_extensions(extensions)
    if partition:
        runner.add_partition(partition)

    for e in env:
        runner.add_env(*e)
    return runner.build_cmd()


def _start_process(cmd, runner, type, config):
    s = PopenSpawn(cmd, encoding="utf-8", env=runner.get_env(),
                   cwd=resolve_cwd(config), logfile=file(LogService.LOG_FILE, 'a+'))
    click.secho("Started dashbase-{} with pid: {}".format(type, s.proc.pid))
    _health_check(s.proc.pid)


def _health_check(pid):
    system_env = get_process_env(pid)
    localhost_port = "localhost:{}".format(system_env['ADMINPORT'])
    health_checker = DropWizardAdminHealthChecker(localhost_port, NUM_TRIES, DELAY_IN_SECONDS)
    succ = health_checker.check_health()
    if not succ:
        LogService.log('Pid: {}'.format(pid))
        LogService.log('Health check not passed!')
    else:
        click.secho("Health check passed: {}".format(succ))
    health_checker.close()


def _check_java_version():
    # will return digits like 1.7 or 1.8
    cmd = '''java -version 2>&1 | grep -i version | cut -d'"' -f2 | cut -d'.' -f1-2'''
    r = os.popen(cmd)
    java_version = r.readline()
    if not java_version or float(java_version) < 1.8:
        LogService.log('Needs java >= 1.8 to run dashbase.')
        raise CliRuntimeError('Environment Error')
