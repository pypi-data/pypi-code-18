# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

import sys
import os
import subprocess
import tempfile
import textwrap
import errno
# import traceback


import ruamel.yaml
from ruamel.std.pathlib import Path, pushd, popd
from ruamel.showoutput import show_output

from ruamel.dcw import __version__

dbg = int(os.environ.get('DCWDBG', 0))
env_inc = Path('.dcw_env_vars.inc')


class Generate():
    def __init__(self, args, config_dir, docker_compose):
        self._args = args
        self._config_dir = config_dir
        self._docker_compose = docker_compose
        self.etc = self._args.etc

    def generate(self):
        file_name = None
        yaml_file = getattr(self._args, 'yaml-file')
        if yaml_file is None:
            yaml_file = Path('.')
        if yaml_file.is_dir():
            pushd(yaml_file)
            cur_dir = Path('.')
            for ext in 'yml', 'yaml':
                tmp = cur_dir / ('docker-compose.' + ext)
                if tmp.exists():
                    file_name = tmp
                    break
            else:
                tmp = []
                for ext in 'yaml', 'yml':
                    tmp.extend(cur_dir.glob('*' + ext))
                if len(tmp) == 1:
                    file_name = tmp[0]
        else:
            file_name = yaml_file
        assert isinstance(file_name, Path)
        file_name = file_name.resolve()
        data, envs = self._get_data(file_name)
        data['template'] = self._config_dir
        dc = self._docker_compose
        assert dc.exists() and dc.is_file()
        data['dc'] = dc
        if self._args.respawn_limit:
            if self._args.respawn_limit[0] < 0:
                v = 'respawn limit unlimited'
            else:
                v = 'respawn limit {0} {1}\n'.format(*self._args.respawn_limit)
            data['respawnlimit'] = v  # empty string ok
        else:
            data['respawnlimit'] = ''  # empty string ok
        # print(ruamel.yaml.dump(data, allow_unicode=True))

        # data looks like:
        #
        # author: Anthon van der Neut <a.van.der.neut@ruamel.eu>
        # description: Mongo container
        # file: /opt/docker/mongo/docker-compose.yml
        # name: [mongo]   # a list of all container names, used to create service name
        # ports:          # per container name, any *public* ports
        #     mongo: [27017]
        if not self._args.upstart and not self._args.systemd:
            init_service = self.determine_init_service()
            if init_service == 'upstart':
                self._args.upstart = True
            elif init_service == 'systemd':
                self._args.systemd = True
            else:
                print('unknown service', init_service)
                sys.exit(1)
        # print(self._args.upstart, self._args.systemd)
        name = data['description']
        if data['ports']:
            p = set()
            for k in data['ports']:
                p.update(data['ports'][k])
            name += ' on port{} {}'.format('s' if len(p) > 1 else '',
                                           ', '.join([str(x) for x in sorted(p)]))
        data['description'] = name
        if not self._args.no_service_author_info:
            data['author'] += ' (dcw {})'.format(__version__)
        # for k in sorted(data):
        #     print(' ', k, '->', data[k])
        data['envs'] = ''
        if self._args.upstart:
            if envs:
                data['envs'] = '\n'.join(['env {}={}'.format(k, envs[k]) for k in envs])
            self.gen_upstart(data)
        if self._args.systemd:
            if envs:
                data['envs'] = '\n'.join(['Environment={}={}'.format(
                    k, envs[k]) for k in envs]) + '\n'
            self.gen_systemd(data)
            if self._args.install:
                self.install_systemd(data)
            if self._args.start:
                self.start_systemd(data)
            self.status_systemd(data)
        if yaml_file.is_dir():
            popd()

    def diff(self, content, service_file):
        import difflib
        print('service_file', str(service_file))
        print('-' * 80)
        try:
            res = service_file.read_text()
        except OSError as e:
            if e.errno == errno.ENOENT:
                print("service file {}, doesn't exist yet".format(service_file))
        else:
            differ = difflib.Differ()
            result = list(differ.compare(
                res.splitlines(True),
                content.splitlines(True),
            ))
            sys.stdout.write(''.join(result))
        sys.exit(0)

    def gen_upstart(self, data):
        service_file = self.etc / 'init' / ('-'.join(data['name']) +
                                            '-docker.conf')
        template = (data['template'] / 'upstart.template').read_text()
        content = template.format(**data)
        if self._args.diff:
            self.diff(content, service_file)
        print(content)
        tab_exp = self.etc / 'init.d' / ('-'.join(data['name']) + '-docker')
        # this should be the real target, even when testing
        target = Path('/lib/init/upstart-job')
        if tab_exp.exists():
            assert tab_exp.resolve() == target
        # create the file
        td = Path(tempfile.mkdtemp(prefix='tmp_dc2service'))
        tf = td / service_file.name
        tf.write_text(content)
        service_file.parent.mkdir(parents=True, exist_ok=True)
        tab_exp.parent.mkdir(parents=True, exist_ok=True)
        print('>>>> writing', service_file)
        try:
            subprocess.call(['sudo', 'cp', str(tf), str(service_file)])
        except KeyboardInterrupt:
            sys.exit(1)
        td.rmtree()
        # create the link
        if not tab_exp.exists():
            print('>>>> creating', tab_exp)
            subprocess.call(['sudo', 'ln', '-s', str(target), str(tab_exp)])
        print('>>>> start with:')
        print('     sudo start {}'.format(service_file.stem))
        print('>>>> disable service with:')
        print('     echo manual | sudo tee /etc/init/{}.override'.format(service_file.stem))
        self.print_rebuild()

    def gen_systemd(self, data):
        service_file = self.etc / 'systemd' / 'system' / ('-'.join(data['name']) +
                                                          '-docker.service')

        template_file = data['template'] / 'systemd.template'
        template = template_file.read_text()
        up_d = u'up -d --no-recreate'
        if up_d in template and not self._args.up_d:
            for nr, line in enumerate(template.splitlines()):
                if up_d not in line:
                    continue
                if not line.startswith(u"ExecStart"):
                    continue
                print('Found "{}" in template {} (line: {})'.format(
                    up_d, template_file, nr))
                print('which is probably not ok. Remove the template file to have it updated,')
                print('edit it, or specify "--up-d" on the commandline')
            sys.exit(0)
        content = template.format(**data)
        if self._args.diff:
            self.diff(content, service_file)
        print(content)
        td = Path(tempfile.mkdtemp(prefix='tmp_dc2service'))
        tf = td / service_file.name
        tf.write_text(content)
        service_file.parent.mkdir(parents=True, exist_ok=True)
        print('>>>> writing', service_file)
        try:
            subprocess.call(['sudo', 'cp', str(tf), str(service_file)])
        except KeyboardInterrupt:
            sys.exit(1)
        td.rmtree()
        print('>>>> start with:')
        print('     sudo systemctl start {}'.format(service_file.stem))
        print('>>>> enable on reboot with:')
        print('     sudo systemctl enable {}'.format(service_file.stem))
        self.print_rebuild()

    def install_systemd(self, data):
        service_name = '-'.join(data['name']) + '-docker.service'
        cmd = ['sudo', 'systemctl', 'enable', str(service_name)]
        try:
            subprocess.call(cmd)
        except KeyboardInterrupt:
            sys.exit(1)

    def start_systemd(self, data):
        service_name = '-'.join(data['name']) + '-docker.service'
        cmd = ['sudo', 'systemctl', 'restart', str(service_name)]
        print('cmd:', ' '.join(cmd))
        try:
            subprocess.call(cmd)
        except KeyboardInterrupt:
            sys.exit(1)

    def status_systemd(self, data):
        service_name = '-'.join(data['name']) + '-docker.service'
        cmd = ['systemctl', 'status', str(service_name)]
        print('cmd:', ' '.join(cmd))
        try:
            subprocess.call(cmd)
        except KeyboardInterrupt:
            sys.exit(1)

    def print_rebuild(self):
        executable = self._docker_compose.name
        msg = textwrap.dedent("""\
        You can use '{} build' to create a new image, which will be used after the
        next restart (or reboot). If no new image is there, the container is not
        recreated""".format(executable))
        print(textwrap.fill(msg))

    def _get_data(self, dc_file):
        yaml_str = dc_file.read_text()
        print(yaml_str)
        my_env = os.environ.copy()
        # first read in to set base environment vars
        _data = ruamel.yaml.load(yaml_str, Loader=ruamel.yaml.RoundTripLoader)
        base_env = _data.get('user-data', {'env-defaults': {}}).get('env-defaults', {})
        for k in base_env:
            if k not in my_env:
                my_env[k] = base_env[k]
        envs = {}
        if '${' in yaml_str:
            for part in yaml_str.split('${')[1:]:
                k = part.split('}', 1)[0]
                if not my_env:
                    envs[k] = os.environ.get(k, 'ENV_{}_NOT_FOUND'.format(k))
            yaml_str = yaml_str.replace('${', '{').format(**my_env)
        _data = ruamel.yaml.load(yaml_str, Loader=ruamel.yaml.RoundTripLoader)
        for k1 in _data:
            if k1 == 'version':
                version = _data.get('version')
            else:
                version = 1
            break
        assert isinstance(_data, ruamel.yaml.comments.CommentedMap)
        ret_val = {}
        error = False
        user_data = _data.get('user-data')
        if user_data:
            if 'author' in user_data:
                ret_val['author'] = user_data['author']
            if 'description' in user_data:
                ret_val['description'] = user_data['description']
        else:
            try:
                pre_comments = _data.ca.comment[1]
            except Exception as e:
                print(e)
                print('\nexception retrieving metadata comments from', dc_file)
                sys.exit(1)
            for pre_comment in pre_comments:
                if 'author:' in pre_comment.value:
                    ret_val['author'] = pre_comment.value.split(':', 1)[1].strip()
                if 'description:' in pre_comment.value:
                    ret_val['description'] = pre_comment.value.split(':', 1)[1].strip()
        container_names = []
        external_ports = {}
        services = _data if version == 1 else _data['services']
        for k in services:
            service = services[k]
            if 'container_name' not in service:
                print('service {} in {}, lacks a container_name'.format(k, dc_file))
                error = True
            else:
                name = service['container_name']
                container_names.append(name)
            for p in service.get('ports', []):
                if ':' in p:
                    external_ports.setdefault(name, []).append(int(p.split(':')[0]))
        # we need to have a description and a responsible person
        if 'author' not in ret_val:
            print('no author comment found in {}'.format(dc_file))
            error = True
        if 'description' not in ret_val:
            print('no author comment found in {}'.format(dc_file))
            error = True
        if error:
            sys.exit(1)
        ret_val['name'] = container_names
        ret_val['ports'] = external_ports
        ret_val['file'] = dc_file
        return ret_val, envs

    def determine_init_service(self):
        """check OS for service type used """
        if 'systemd' in Path('/sbin/init').resolve().name:
            return 'systemd'
        try:
            res = subprocess.check_output(['/sbin/init', '--version']).decode('utf-8')
            if u'upstart' in res:
                return 'upstart'
        except subprocess.CalledProcessError as e:
            print('cannot determine init service\n', e.output, sep='')
            sys.exit(1)
        print('cannot determine init service\n', res, sep='')
        sys.exit(1)

    def templates(self):
        for name in self._config_dir.glob('*.template'):
            print(name.resolve())


class DockerComposeWrapper(object):
    def __init__(self):
        self._args = None
        self._file_name = None
        self._data = None
        if self.docker_compose is None:
            print(sys.path)
            print('docker-compose not found in path')
            if os.environ.get('USER') in ['anthon', 'avanderneut']:
                print('\n>>>> for debugging/development see Makefile <<<<\n')
            sys.exit(1)

    @property
    def docker_compose(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            for p in ['/opt/util/docker-compose/bin'] + sys.path:
                for exe in ['dcw', 'docker-compose']:
                    pp = os.path.join(p, 'dcw')
                    if dbg > 0:
                        print('pp', pp)
                    if os.path.exists(pp):
                        d = Path(pp)
                        setattr(self, attr, d)
                        return d
            setattr(self, attr, None)
        return getattr(self, attr)

    def _find_docker_compose(self):
        return None

    @property
    def config_dir(self):
        # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            d = Path(os.environ.get('XDG_CONFIG_HOME',
                                    os.path.join(os.environ['HOME'], '.config')))
            d /= 'ruamel_dcw'
            d.mkdir(parents=True, exist_ok=True)
            setattr(self, attr, d)
            return d
        return getattr(self, attr)

    def process_args(self, args):
        if (len(args) > 1) and args[0] in ['-f', '--file']:
            self._file_name = self.find_yaml(args[1])
            self._args = args[2:]
        elif (len(args) > 0) and (args[0].startswith('--file=') or args[0].startswith('-f=')):
            self._file_name = self.find_yaml(args[0].split('=', 1)[1])
            self._args = args[1:]
        else:
            self._file_name = Path('docker-compose.yml')
            self._args = args

    def find_yaml(self, name):
        for file_name in [
            Path(name),                                         # full path
            Path(name) / 'docker-compose.yml',                  # base dir
            Path('/opt/docker') / name / 'docker-compose.yml',  # standard docker dir
        ]:
            if file_name.exists():
                # print('Found', file_name)
                file_name.parent.chdir()
                return file_name

    def load_yaml(self):
        with self._file_name.open() as fp:
            self._data = ruamel.yaml.load(fp, Loader=ruamel.yaml.RoundTripLoader)

    def set_os_env_defaults(self):
        envs = self._data.get('user-data', {}).get('env-defaults')
        if envs is None:
            return
        # some values that can be <named in
        host_name_file = Path('/etc/hostname')
        lookup = {}
        lookup['hostname'], lookup['domain'] = host_name_file.read_text().strip().split('.', 1)
        # assume hostname is in the hosts file
        hosts_file = Path('/etc/hosts')
        for line in hosts_file.read_text().splitlines():
            sline = line.split('#')[0].split()
            if lookup['hostname'] in sline:
                lookup['hostip'] = sline[0]
        if 'hostip' not in lookup:
            print('hostname not found in /etc/hosts')
            sys.exit(1)
        for line in subprocess.check_output(['ip', 'addr', 'show']).decode(
                'utf-8').splitlines():
            if lookup['hostip'] in line and 'global' in line:
                interface = line.split('global')[1].strip()
                lookup['hosteth'] = interface
        # print(lookup)
        fp = None
        if not env_inc.exists() or (env_inc.stat().st_mtime <
                                    self._file_name.stat().st_mtime):
            print('writing', str(env_inc))
            fp = env_inc.open('w')
        for k in envs:
            if k not in os.environ:
                value = str(envs[k])
                if value and value[0] == '<':
                    value = lookup.get(value[1:], value)
                os.environ[k] = value  # str for those pesky port numbers
            if fp:
                fp.write(u'export {}="{}"\n'.format(k, os.environ[k]))
        if fp:
            fp.close()
        # print(env_inc.read_text())
        # sys.exit(1)

    def write_temp_file_call_docker_compose(self):
        odata = self.rewrite_data()
        sys.argv = [str(self.docker_compose)]
        alt_yaml = Path('.dcw_alt.yml')
        ruamel.yaml.round_trip_dump(odata, stream=alt_yaml.open('wb'),
                                    encoding='utf-8')
        sys.argv.append('--file={}'.format(alt_yaml))
        sys.argv.extend(self._args)
        self.call_docker_compose()

    def call_docker_compose(self):
        try:
            import compose.cli.main
        except ImportError:
            lib = self.docker_compose.parent.parent / 'lib'
            lib = list(lib.glob('python*/site-packages/compose'))
            if lib:
                sys.path.insert(0, str(lib[0].parent))
                try:
                    import compose.cli.main
                except:
                    print(sys.path)
                    raise
        if dbg > 0:
            print('compose loc', compose.cli.main.__file__)
        compose.cli.main.main()

    def rewrite_data(self):
        odata = ruamel.yaml.comments.CommentedMap()
        for k in self._data:
            try:
                if k == 'user-data' or k.startswith('user-data-'):
                    continue
            except TypeError:
                pass
            odata[k] = self._data[k]
        return odata

    def run_truncate(self):
        # dc ps -q -> id of container
        alt_yaml = Path('.dcw_alt.yml')
        cid = show_output([self.docker_compose, '--file={}'.format(alt_yaml), 'ps', '-q'],
                          verbose=-1).rstrip()
        print(cid)
        path = Path('/var/lib/docker/containers/{}/{}-json.log'.format(cid, cid))
        cmd = 'sudo truncate -s 0 ' + str(path)
        # print(cmd)
        os.system(cmd)
        # res = show_output(['sudo', 'truncate', '-s ', str(path)])

    def run_bash(self):
        odata = self.rewrite_data()
        # first of the services
        for x in odata['services']:
            name = odata['services'][x].get('container_name')
            if not name:
                raise NotImplementedError
            if name.startswith('${') and name.endswith('}'):
                name = os.environ.get(name[2:-1])
            os.system('docker exec -it {} /bin/bash'.format(name))

    def volume_test(self, create=True):
        for service in self._data.get('services', []):
            final_slash = False
            volumes = []
            for volume in self._data['services'][service].get('volumes', []):
                d = volume.split(':')[0].replace('${', '{').format(**os.environ)
                if d[-1] == '/':
                    final_slash = True
                volumes.append(d)
            for volume in volumes:
                d = Path(volume)
                # print('d', d, d.exists())
                if create is False:
                    if final_slash:
                        if volume[-1] == '/':
                            if d.exists() and not d.is_dir():
                                print('{} should be a directory according to YAML'.format(
                                    volume))
                            elif not d.exists():
                                print('creating directory {}'.format(d))
                            else:
                                print('existing directory {}'.format(d))
                        else:
                            if d.exists() and d.is_dir():
                                print('{} should be a file according to YAML'.format(volume))
                            elif not d.exists():
                                print('creating file {}'.format(volume))
                            else:
                                print('existing file {}'.format(d))
                        continue
                    # check that all exist and complain that there is no dir/file info if not
                    if not d.exists():
                        print('>>>>> do not know how to create {} <<<<'.format(d))
                    else:
                        print('existing {}{}'.format(d, '/' if d.is_dir() else ''))
                    continue
                # create only if final_slash, otherwise assume docker does
                # this (and makes dirs)
                if not final_slash:
                    break
                if d.exists():
                    if volume[-1] == '/' and not d.is_dir():
                        print('{} should be a directory according to YAML'.format(volume))
                    if volume[-1] != '/' and d.is_dir():
                        print('{} should be a file according to YAML'.format(volume))
                    continue
                if volume[-1] == '/':
                    d.mkdir(parents=True)
                else:
                    d.parent.mkdir(parents=True, exist_ok=True)
                    d.write_bytes(b'')

    def run(self):
        dcw = False
        if self._args and self._args[0].startswith('dcw-'):
            self._args = self._args[0][4:]
            dcw = True
        dcw = dcw  # temporary to use it without getting warning
        # should check if it is a docker-compose command first
        if len(self._args) < 1:
            self._args = ['--help']
        if self._args[0] == 'expand':
            ruamel.yaml.round_trip_dump(self.rewrite_data(), stream=sys.stdout,
                                        encoding='utf-8')
            print('------ env:')
            if env_inc.exists():
                with env_inc.open() as fp:
                    print(fp.read())
            else:
                print('    file not found')
            if len(self._args) > 1 and self._args[1] == '--test':
                print('------ testing volumes:')
                self.volume_test(create=False)
            return 0
        if self._args[0] == 'truncate':
            self.run_truncate()
            return 0
        if self._args[0] == 'bash':
            self.run_bash()
            return 0
        self.volume_test()
        return self.write_temp_file_call_docker_compose()

    # the following methods don't need docker-compose.yaml to exist
    def generate_asked(self):
        # should test for generate or service, if service do install and start
        # as well
        if len(sys.argv) == 1 or sys.argv[1] != 'generate':
            return False
        import argparse
        self.set_templates()
        parser = argparse.ArgumentParser(prog='docker-compose generate')
        parser.add_argument('--verbose', '-v', action='store_const',
                            help='increase verbosity level',
                            const=1, default=0)
        parser.add_argument('--upstart', action='store_true',
                            help='generate upstart file (instead of autodetect)')
        parser.add_argument('--systemd', action='store_true',
                            help='generate systemd file (instead of autodetect)')
        parser.add_argument(
            '--docker-compose', metavar='EXE',
            help='path to dcw/docker-compose %(metavar)s (default %(default)s)')
        parser.add_argument('--respawn-limit', nargs=2, type=int)
        parser.add_argument('--no-service-author-info', action='store_true')
        parser.add_argument('--up-d', action='store_true',
                            help='allow (old) "up -d" in ExecStart line')
        parser.add_argument('--etc', default=Path('/etc/'), type=Path,
                            help='set base dir (default %(default)s)')
        parser.add_argument('--diff', action='store_true',
                            help="diff generated service with existing one (no install)")
        parser.add_argument('--install', action='store_true',
                            help="install the service")
        parser.add_argument('--start', action='store_true',
                            help="start the service")
        parser.add_argument('yaml-file', nargs='?', type=Path,
                            help='optional defaults to docker-compose.yaml')
        args = parser.parse_args(sys.argv[2:])
        gen = Generate(args, self.config_dir, self.docker_compose)
        gen.generate()
        return True

    def list_templates_asked(self):
        if len(sys.argv) == 1 or sys.argv[1] != 'templates':
            return False
        self.set_templates()
        print('templates:')
        for name in self.config_dir.glob('*.template'):
            print(' ', name.resolve())
        return True

    def set_templates(self):
        """copy all templates from installation to config directory"""
        msg = True
        for template in Path(__file__).with_name('_templates').glob('*'):
            target = self.config_dir / (template.stem + '.template')
            if not target.exists():
                if msg:
                    print('setting up templates')
                    msg = False
                template.copy(target)

    def help_asked(self):
        """return true if help found in arguments"""
        if '-h' in sys.argv[1:] or '--help' in sys.argv[1:]:
            return True
        return False

    def version_asked(self):
        """return true if help found in arguments"""
        if 'version' in sys.argv[1:] or '--version' in sys.argv[1:]:
            print('dcw version:', __version__)
            return True
        return False


def wrapped_main():
    if dbg > 0:
        print('----------DEBUG ACTIVE------------------')

    dcw = DockerComposeWrapper()
    dcw.process_args(sys.argv[1:])
    # some special handling
    if dcw.version_asked():
        sys.argv[1:] = ['version']
        dcw.call_docker_compose()
        res = 0
    elif dcw.generate_asked():  # before help, as it has its own sub-help
        if dbg > 0:
            print('dcw.generate_asked()')
        res = 0
    elif dcw.help_asked():
        if dbg > 0:
            print('dcw.help_asked()')
        try:
            dcw.call_docker_compose()
        except SystemExit as e:
            if e.code in [0, None] and sys.argv[1] in ['-h', '--help']:
                for cmd, hlp in sorted((
                        ('bash', 'run bash in container'),
                        ('expand', 'show expanded YAML and {}'.format(env_inc)),
                        ('generate', 'generate systemd/upstart auto startup file'),
                        ('templates', 'list files used as template'),
                        ('truncate', 'truncate log file (needs sudo)'),
                )):
                    print(' *{:<18s} {}'.format(cmd, hlp))
                print('\n *: ruamel.dcw extensions')
        res = 0
    elif dcw.list_templates_asked():
        res = 0
    else:
        dcw.load_yaml()
        dcw.set_os_env_defaults()
        res = dcw.run()
    sys.exit(res)


def main():
    return wrapped_main()
    # import daemon
    # with daemon.DaemonContext():
    #     wrapped_main()

if __name__ == "__main__":
    main()
