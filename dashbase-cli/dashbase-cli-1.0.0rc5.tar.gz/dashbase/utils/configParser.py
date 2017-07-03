import os

import yaml

from dashbase.cli.constants import (DashbaseService, DEFAULT_MIRROR,
                                    DASHBASE_DEFAULT_CONF_DIR,
                                    DASHBASE_MONITOR_CONFIG)
from dashbase.cli.models import Service, Host
from dashbase.services import VersionService
from dashbase.utils.errors import CliRuntimeError


class ConfigParser(object):
    def __init__(self, src, default=None):
        if default is None:
            default = {}
        self.default = default
        self.data = {}
        if isinstance(src, str):
            src = [src]
        if not isinstance(src, list):
            raise AssertionError("Invalid value for src; must be a str or list.")
        for file in src:
            if os.path.isfile(file):
                with open(file) as f:
                    self.data = yaml.load(f)
                    if not self.data:
                        raise CliRuntimeError(
                            "parse config `{}` error. Please make sure the config is a correct yaml file.".format(file))
                break

    def get(self, key, default=None):
        if key in self.data:
            return self.data[key]
        if key in self.default:
            return self.default[key]
        if default:
            return default
        return ""

    def set(self, key, value):
        self.data[key] = value


class ClusterConfigParser(object):
    def __init__(self, src):
        self.config = ConfigParser(src=src)
        self.prefix = None
        self.zookeeper_url = None
        self.mirror = None
        self.services = {}  # dict of services by name
        self.hosts = {}  # dict of hosts by name
        self.uninstall = False
        self.version = None
        self.available_versions = []

    def parse(self):
        self._parse_toplevel()
        self._parse_services()
        self._parse_hosts()

    def _parse_toplevel(self):

        mirror_url = DEFAULT_MIRROR
        if 'mirror' in self.config.data:
            self.mirror = self.config.data['mirror']
            mirror_url = self.mirror

        self.available_versions = VersionService.get_available_versions(mirror_url)

        if 'uninstall' in self.config.data:
            self.uninstall = self.config.data['uninstall']
            if not isinstance(self.uninstall, bool):
                raise CliRuntimeError('`uninstall` in dashbase.yml should be `true` or `false`.')

        if 'version' in self.config.data:
            self.version = self.config.data['version']
            self.check_version(self.version)

        _exists('prefix', self.config.data, "missing `prefix` in dashbase.yml")
        self.prefix = self.config.data['prefix']

        if 'zookeeper_url' in self.config.data:
            self.zookeeper_url = self.config.data['zookeeper_url']

        _exists('services', self.config.data, "missing `services` in dashbase.yml")
        _exists('hosts', self.config.data, "missing `hosts` in dashbase.yml")
        return True

    def get_config_path(self, values, key):
        if values["type"] == DashbaseService.MONITOR:
            monitor_config_file = os.path.join(DASHBASE_DEFAULT_CONF_DIR, DASHBASE_MONITOR_CONFIG)
            if 'config' in values:
                monitor_config_file = self._resolve_path(values['config'], "invalid config path for {}.".format(key))
            if not os.path.isfile(monitor_config_file):
                from dashbase.cli.cmd.install import download_from_url
                latest_version = VersionService.get_latest_version(DEFAULT_MIRROR)
                url = "{mirror}/{version}/{monitor_config}".format(mirror=DEFAULT_MIRROR, version=latest_version,
                                                                   monitor_config=DASHBASE_MONITOR_CONFIG)
                download_from_url(url, monitor_config_file)

            return monitor_config_file
        else:
            _exists('config', values, "missing `config` specification for service `{}`.".format(key))
            return self._resolve_path(values['config'], "missing config file for service `{}`.".format(key))

    def _parse_services(self):
        dashbase_service = self.config.data['services']
        for key, values in list(dashbase_service.items()):
            # for each service
            _exists('type', values, "missing `type` for service {}".format(key))
            config = self.get_config_path(values, key)
            d_service = Service(data={'name': key,
                                      'type': values['type'],
                                      'port': None,
                                      'admin_port': None,
                                      'heap_opts': "-Xmx1g -Xms1g -XX:NewSize=512m",  # default heap_opt
                                      'config': config,
                                      'host': '',
                                      'env': {},
                                      'partition': None})
            # append prefix if exists
            if self.prefix:
                d_service.set_val('name', "{}-{}".format(self.prefix, key))

            d_service.set_val('version', self.version)
            if 'version' in values:
                self.check_version(values['version'])
                d_service.set_val('version', values['version'])

            if 'env' in values:
                d_service.set_val('env', values['env'])

            # export ZooKeeper as env if exists,
            # but do not replace if specified in service env
            envs = d_service.get_val('env')
            if self.zookeeper_url and 'ZOOKEEPER_URL' not in envs:
                envs['ZOOKEEPER_URL'] = self.zookeeper_url
                d_service.set_val('env', envs)

            if values['type'] in (DashbaseService.MONITOR, DashbaseService.TABLE):
                # service is a table or monitor, parse partitions
                err_message = "missing `{}` for table {} defaults"
                _exists('defaults', values, "missing `defaults` for table {}".format(key))
                _exists('partitions', values, "missing `partitions` for table {}".format(key))
                defaults = values['defaults']
                _exists('host', defaults, err_message.format("host", key))
                _exists('port', defaults, err_message.format("port", key))
                _exists('admin_port', defaults, err_message.format("admin_port", key))
                if 'heap_opts' in defaults:
                    d_service.set_val('heap_opts', defaults['heap_opts'])
                name = d_service.get_val('name')

                for partition, confs in list(values['partitions'].items()):
                    # for each partition
                    p_service = Service(data=d_service.get())
                    p_service.set_val('name', "{}-{}".format(name, partition))
                    p_service.set_val('partition', partition)
                    # set defaults
                    p_service.set_val('host', defaults['host'])
                    p_service.set_val('port', defaults['port'])
                    p_service.set_val('admin_port', defaults['admin_port'])

                    if confs:  # partition has no mappings, use default
                        # override defaults if exists
                        if 'host' in confs:
                            p_service.set_val('host', confs['host'])
                        if 'port' in confs:
                            p_service.set_val('port', confs['port'])
                        if 'admin_port' in confs:
                            p_service.set_val('admin_port', confs['admin_port'])
                        if 'heap_opts' in confs:
                            p_service.set_val('heap_opts', confs['heap_opts'])
                        if 'env' in confs:
                            new_env = confs['env']
                            old_env = p_service.get_val('env')
                            for env in new_env:
                                old_env[env] = new_env[env]
                            p_service.set_val('env', old_env)
                    self.services[p_service.get_val('name')] = p_service
                continue

            # set host, port, admin_port values if exist
            _exists('host', values, "missing `host` for service {}".format(key))
            d_service.set_val('host', values['host'])
            _exists('port', values, "missing `port` for service {}".format(key))
            d_service.set_val('port', values['port'])
            _exists('admin_port', values, "missing `admin_port` for service {}".format(key))
            d_service.set_val('admin_port', values['admin_port'])
            # override default heap_opts if exist
            if 'heap_opts' in values:
                d_service.set_val('heap_opts', values['heap_opts'])

            self.services[d_service.get_val('name')] = d_service
        return True

    def _parse_hosts(self):
        dashbase_hosts = self.config.data['hosts']
        for key, values in list(dashbase_hosts.items()):
            _exists('hostname', values, "missing `hostname` for host {}".format(key))
            _exists('username', values, "missing `username` for host {}".format(key))
            _exists('private_key', values, "missing `private_key` for host {}".format(key))
            pkey = self._resolve_path(values['private_key'],
                                      "host private_key is invalid. Please specify the path to a valid key file.")

            d_host = Host(data={'name': key,
                                'hostname': values['hostname'],
                                'username': values['username'],
                                'private_key': pkey})

            self.hosts[d_host.get_val('name')] = d_host
        return True

    @staticmethod
    def _resolve_path(path, error_msg="path does not exist."):
        if not path:
            raise CliRuntimeError(error_msg)
        if path.startswith("~"):
            path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        if not os.path.exists(path):
            print(path)
            raise CliRuntimeError(error_msg)
        if not os.path.isfile(path):
            print(path)
            raise CliRuntimeError(error_msg)
        return path

    def check_version(self, version):
        VersionService.check_version(version, available_versions=self.available_versions)


class ServiceConfigParser(object):
    def __init__(self, src):
        self.config = ConfigParser(src=src)
        self.app_connectors = {}
        self.admin_connectors = {}

    def parse(self):
        server = self._parse_server()
        self._parse_connectors(server)

    def _parse_server(self):
        _exists('server', self.config.data, "`server` missing from configs.")
        server = self.config.data['server']

        _exists('applicationContextPath', server, "applicationContextPath is required.")
        _exists('adminContextPath', server, "applicationContextPath is required.")
        return server

    def _parse_connectors(self, server):

        def do_parse_connector(name, connector):
            temp = {}
            if not isinstance(connector, list):
                raise TypeError("Specified {} must be a list of connectors. e.g.\n"
                                " - type: http\n   port: 1234".format(name))
            for con in connector:
                if not _exists('type', con, "missing `type` in {}".format(name)) or con['type'] is None:
                    raise KeyError("type value missing for {}.".format(name))
                if not _exists('port', con, "missing `port` in {}".format(name)) or con['port'] is None:
                    raise KeyError("port value missing for {}.".format(name))
                temp[con['type']] = con['port']
            return temp

        if 'applicationConnectors' not in server:
            self.app_connectors['http'] = 8080
            self.app_connectors['https'] = 8443
        else:
            app_connectors = server['applicationConnectors']
            self.app_connectors = do_parse_connector('applicationConnectors', app_connectors)
            if 'https' not in self.app_connectors:
                self.app_connectors['https'] = 8443
        if 'adminConnectors' not in server:
            self.admin_connectors['http'] = 8081
            self.admin_connectors['https'] = 8444
        else:
            admin_connectors = server['adminConnectors']
            self.admin_connectors = do_parse_connector('adminConnectors', admin_connectors)
            if 'https' not in self.admin_connectors:
                self.admin_connectors['https'] = 8444

    @staticmethod
    def get_connector_port(connector, protocol):
        """Returns the port for the specified protocol in connector. If the
        protocol is an env variable, returns False."""
        _exists(protocol, connector, "`{}` not found in connector.".format(protocol))
        if str(connector[protocol]).startswith('$'):  # is an env variable
            return False
        return connector[protocol]


def _exists(key, dictionary, error_msg):
    """Helper function to check if key exists in dictionary.
    If not, raise a KeyError with given error message."""
    if key not in dictionary:
        raise CliRuntimeError(error_msg)
    return True
