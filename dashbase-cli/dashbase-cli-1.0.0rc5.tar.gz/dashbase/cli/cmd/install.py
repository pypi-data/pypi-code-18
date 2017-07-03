import os

import click
import requests
from tqdm import tqdm

from dashbase.cli.cli import pass_context, root
from dashbase.cli.constants import (list_services,
                                    ZOOKEEPER,
                                    DEFAULT_ZOOKEEPER_MIRROR, DASHBASE_EXTENSIONS)
from dashbase.cli.utils import extract_tar
from dashbase.services import JarService, VersionService
from dashbase.utils.errors import CliRuntimeError, NotFound, handle_network_error


def download_dashbase(type, home, version, mirror):
    if type == DASHBASE_EXTENSIONS:
        click.secho("Downloading {} for version {}".format(type, version))
        package = "{}.tar.gz".format(DASHBASE_EXTENSIONS)
        url = "{}/{}/{}".format(mirror, version, package)
        dst = os.path.join(home, package + ".download")
    else:
        jarName = JarService.get_jar_name(type, version)
        click.secho("Downloading {}".format(jarName))

        url = "{mirror}/{version}/{jarName}".format(mirror=mirror,
                                                    version=version,
                                                    jarName=jarName)
        dst = os.path.join(home, "dashbase-{type}/target/{jarName}.download".format(type=type,
                                                                                    jarName=jarName))

    download_from_url(url, dst)
    #  TODO verify downlaod
    os.rename(dst, dst[:-(len(".download"))])


def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    req = requests.get(url, allow_redirects=True, stream=True)
    handle_network_error(url, req.status_code)

    file_size = int(req.headers.get('Content-Length', -1))
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(total=file_size, initial=first_byte,
                unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)

    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


@root.group(chain=True)
@pass_context
def cmd_install(ctx):
    """Install a Dashbase service or ZooKeeper"""
    pass


@cmd_install.command('service', short_help='Install a Dashbase service.')
@click.argument('type', nargs=1, type=click.Choice(list_services()))
@pass_context
def cmd_install_service(ctx, type):
    """Download a Dashbase service jar"""
    home = ctx.config.get('home', '')
    mirror = ctx.config.get('mirror')
    version = ctx.config.get('version', VersionService.get_latest_version(mirror))

    try:
        installed_versions, selected_version = JarService.get_jar_versions(home_path=home, type=type, exception=True)
    except NotFound:
        installed_versions = None

    install_version = VersionService.get_latest_version(mirror)
    if version:
        available_versions = VersionService.get_available_versions(mirror)
        if version not in available_versions:
            raise CliRuntimeError("version `{}` of dashbase-{} is not available.".format(version, type))
        install_version = version

    if installed_versions:
        if install_version in installed_versions:
            click.secho("Version `{}` of dashbase-{} is already installed.".format(install_version, type))
            return
    download_dashbase(type=type, home=home, version=install_version, mirror=mirror)
    click.secho("Successfully installed `{}` of dashbase-{}.".format(install_version, type))


@cmd_install.command(ZOOKEEPER, help="Install ZooKeeper")
@pass_context
def cmd_install_zookeeper(ctx):
    """Install ZooKeeper"""
    home = ctx.config.get("home", "")
    if os.path.exists(os.path.join(home, ZOOKEEPER)):
        click.secho("ZooKeeper is already installed.")
        return
    package = "{}.tar.gz".format(ZOOKEEPER)
    url = DEFAULT_ZOOKEEPER_MIRROR + package
    dst = os.path.join(home, "{}.download".format(package))
    download_from_url(url, dst)
    os.rename(dst, dst[:-(len(".download"))])
    extract_tar(home, package)
    click.secho("Successfully installed ZooKeeper.")


@cmd_install.command('extensions', help="Install Dashbase extensions.")
@pass_context
def cmd_install_extensions(ctx):
    """Install Dashbase Extensions"""
    home = ctx.config.get("home", "")
    mirror = ctx.config.get('mirror')

    if os.path.exists(os.path.join(home, DASHBASE_EXTENSIONS)):
        click.secho("{} is already installed.".format(DASHBASE_EXTENSIONS))
        return
    download_dashbase(DASHBASE_EXTENSIONS, home, VersionService.get_latest_version(mirror), mirror)
    extract_tar(home, "{}.tar.gz".format(DASHBASE_EXTENSIONS))
    click.secho("Successfully installed Dashbase extensions.")
