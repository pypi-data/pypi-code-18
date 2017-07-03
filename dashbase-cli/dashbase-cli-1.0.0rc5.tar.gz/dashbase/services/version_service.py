# -*- coding:utf-8 -*-
import click
import requests

from dashbase.services import LogService
from dashbase.utils.errors import handle_network_error, CliRuntimeError, NetworkError


class VersionService(object):
    """
    Dashbase Version Service
    """

    @classmethod
    def get_manifest_version(cls, mirror):
        version_url = "{mirror}/manifest.json".format(mirror=mirror)
        req = requests.get(version_url, allow_redirects=True)
        handle_network_error(version_url, req.status_code)
        try:
            return req.json()
        except ValueError:
            LogService.log('Can\'t fetch version info.')
            LogService.log('Please check if you have specified the correct mirror or have the necessary permissions.')
            LogService.log('You may need to contact your administrator or support for more information.')
            raise CliRuntimeError('Fetch Version Info Error')

    @classmethod
    def get_latest_version(cls, mirror):
        try:
            manifest = cls.get_manifest_version(mirror)
            latest_version = manifest["latest"]
        except NetworkError as e:
            LogService.log("{} please try again.".format(e.message))
            return
        except AttributeError:
            LogService.log("Unable to get latest version, please try again.")
            return
        return latest_version

    @classmethod
    def get_available_versions(cls, mirror):
        try:
            manifest = cls.get_manifest_version(mirror)
            available_versions = manifest["versions"]
        except NetworkError as e:
            LogService.log("{} please try again.".format(e.message))
            return
        except AttributeError:
            LogService.log("Unable to get available versions, please try again.")
            return
        return available_versions

    @classmethod
    def check_version(cls, version, available_versions=None, mirror=None):
        if not available_versions:
            available_versions = cls.get_available_versions(mirror)

        if version not in available_versions:
            click.secho('Available versions are:', fg='yellow')
            for version in available_versions:
                click.secho(version, fg='yellow')
            raise CliRuntimeError('version:`{}` not available. '
                                  'Please check your config.'.format(version))
