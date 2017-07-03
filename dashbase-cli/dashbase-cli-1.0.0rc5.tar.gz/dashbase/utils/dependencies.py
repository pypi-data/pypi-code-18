# -*- coding:utf-8 -*-
import click
from dashbase.cli.utils import echo_without_newline
from dashbase.services import LogService
from dashbase.utils.errors import CliRuntimeError

APT_CLI = 'sudo apt-get update && sudo apt-get install -y software-properties-common && sudo add-apt-repository -y ppa:webupd8team/java && sudo apt-get update && echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections && sudo apt-get install -y build-essential libssl-dev openjdk-8-jre-headless python python-pip libffi-dev python-dev gcc g++'

YUM_CLI = 'sudo yum -y update && sudo yum -y install gcc gcc-c++ kernel-devel python-devel libxslt-devel libffi-devel openssl-devel java-1.8.0-openjdk'


def install_dependencies(ssh):
    ret, _ = ssh.run('apt-get')
    if ret == 1:
        ret, output = ssh.run(APT_CLI, echo_without_newline)
        if ret != 0:
            LogService.log(output, show=False)
            raise CliRuntimeError('Unable to install necessary dependencies on remote host.')
        return
    ret, _ = ssh.run('yum')
    if ret == 1:
        ret, output = ssh.run(YUM_CLI, echo_without_newline)
        if ret != 0:
            LogService.log(output, show=False)
            raise CliRuntimeError('Unable to install necessary dependencies on remote host.')
    click.secho('Unable to install necessary dependencies automatically on remote host.', fg='yellow')
    click.secho('Please manually install them according to the document.', fg='yellow')
    click.secho('You may need to contact your administrator or support for more information.', fg='yellow')
