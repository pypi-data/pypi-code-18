#!/usr/bin/env python3
"""
OCEAN.

A home-made utility to manage containerised development and testing environments,
between developpers and production.
"""

import bz2
import hashlib
import json
import logging
import os
import random
import re
import shutil
import subprocess
import sys
import textwrap
import time
import traceback
from hashlib import md5

import docker
import yaml
from Crypto.Cipher import AES
from OpenSSL.crypto import FILETYPE_PEM, X509, load_publickey, verify

from .utils import (deepcopy, readlinkabs, rec_rep, recupdate, soft_update,
                    xgetattr, xhasattr)

try:
    from io import StringIO
except BaseException:
    try:
        from cStringIO import StringIO
    except BaseException:
        from StringIO import StringIO

logging.getLogger().setLevel("DEBUG")

if sys.version_info[0] == 2:
    import functools32 as functools
else:
    import functools

# we currently prefer using CLI as it easier to have static linking for "atlantis"
# import docker
# client = docker.from_env(assert_hostname=False)
# print client.version()


if os.isatty(0):
    TI = "-ti"
else:
    TI = "-i"

OCEAN_RANDOM = "%03d%03d%03d" % (random.randint(0, 999),
                                 random.randint(0, 999),
                                 random.randint(0, 999)
                                 )
OCEAN_NAME_PREFIX = os.environ.get("OCEAN_NAME_PREFIX", "").replace("%RANDOM%", OCEAN_RANDOM)

#
# ATALNTIS ALLOW TO RUN OCEAN IN OCEAN
DEFAULT_CONFIG = {
    "docker-cmd": "docker"
}
#
SYSTEM_MANIFEST = {
    "devops": {
        "atlantis": {
            "dockerimg": "python:3.5.1",
            "extraargs": [
                "-v $OCEANPATH$:/home/atlantis/ocean",
                "-v /usr/bin/docker:/usr/bin/docker",
                "-v /var/run/docker.sock:/var/run/docker.sock",
                "-e OCEAN_NAME_PREFIX=atl$OCEANRANDOM$-",
                "-e OCEAN_IMG_PREFIX=atl$OCEANRANDOM$-",
                "-e OCEAN_DOCKER_IP=$OCEANIP$",
                "-v /etc/passwd:/etc/passwd:ro",
                "-v /etc/shadow:/etc/shadow:ro",
                "-v /etc/group:/etc/group:ro",
                "-u $UID$",
                "--env DOCKER_OPTS=\"-H tcp://$OCEANIP$:4243 -H unix:///var/run/docker.sock\""
            ]
        }
    }
}


# ##########################################################################
# MAIN SYSTEM VARIABLES AND MODULE LOADING
# ##########################################################################

AP = os.path.dirname(readlinkabs(__file__))

# IN SOME SCENARIO
# THE MP LINKS TO THE MAIN MANIFEST OF THE CURRENT CODE AND IS MEANT TO BE SHARED
# WHILE THE MPL IS MEANT TO BE A LOCAL MANIFEST RELATING TO A SINGLE USER

MP = os.path.abspath(os.environ.get("OCEANPATH", os.path.dirname(AP)))
MPL = os.path.abspath(os.environ.get("OCEANPATH_LOCAL", os.environ.get("OCEANPATH", os.path.dirname(AP))))
# MANIFEST_URL = "git@git@bitbucket.org:wideio/wideio-repository.git"
SRC = os.path.join(MP, "src")
CFG = os.path.join(MP, "cfg")
CFGL = os.path.join(MPL, "cfg")

DEEP_MANIFEST = True

ALL_MIXINS = []
ALL_HANDLERS = []
modules = {}
for x in os.listdir(os.path.join(AP, "modules")):
    if x.endswith(".py"):
        mn = x[:-3]
        module = __import__('ocean.modules.' + mn, fromlist=['ocean', 'modules'])
        modules[mn] = module
        if mn.startswith("mixin_"):
            try:
                ALL_MIXINS.append(module.MixIn)
            except BaseException:
                logging.warning("could not load mixin from : " + x)
        if mn.endswith("_handler"):
            try:
                ALL_HANDLERS.append(module.__handler__)
            except BaseException:
                logging.warning("could not load mixin from : " + x)


# ##########################################################################
# OTHER UTILITIES.
# ##########################################################################

def subprocess_popen(*args, **kwargs):
    """Wrapper to allow eventual logging.
       NOTE: This log is useful to replicate ocean behaviour for user that don't have ocean.
    """
    logging.debug("subprocess popen : %r %r" % (args, kwargs))
    res = subprocess.Popen(*args, **kwargs)
    return res


vca = "CABASEDIR=%s python %s/modules/vca.py -i " % (MP, AP)
dockerip = os.environ.get("OCEAN_DOCKER_IP", "")  # .decode('utf8')
try:
    if dockerip == "":
        if os.path.exists("/proc/sys/net/ipv4/conf/docker0"):
            o, e = subprocess_popen('/sbin/ifconfig docker0', shell=True, stdout=subprocess.PIPE).communicate()
            dockerip = re.match("inet addr:([0-9.]+)",
                                filter(lambda l: ("inet addr:" in l), o.split("\n"))[0].strip()).groups()[0]
    else:
        logging.warning("Unable to find OCEAN_DOCKER_IP")
except BaseException:
    pass


@functools.lru_cache(maxsize=1280)
def ocean__get(ocean, srv, with_img_env=True):
    self = ocean
    section, srv, tag = self._find_section_new(srv)
    cmanifest = self.manifest[section][srv]
    if with_img_env:
        cmanifest = deepcopy(cmanifest)
        if "dockerimg" in cmanifest:
            try:
                r = self._docker.inspect_image(cmanifest["dockerimg"])
                r = r.get("Config", {}).get("Labels", {})
                r = (r.items() if r else [])
                r = [(i[0][6:].lower().replace('_', '-'), json.loads(i[1])["@value"])
                     for i in r if i[0].startswith("OCEAN.")]
                soft_update(cmanifest, dict(r))
            except Exception:
                logging.warning("failed to get additional metadata from artfifact dockerimg for srv: " + str(srv))
                traceback.print_exc()
    return cmanifest


def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length + iv_length]


class AESCipher(object):
    def __init__(self, key, msgdgst='md5'):
        self.bs = 16
        self.key = key
        self.msgdgst = msgdgst

    def decrypt(self, enc):
        assert enc[:8] == b'Salted__'
        salt = enc[8:16]

        # Now create the key and iv.
        key, iv = self.get_key_and_iv(self.key, salt, msgdgst=self.msgdgst)
        if key is None:
            return None

        cipher = AES.new(key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[self.bs:]))  # .decode('utf-8')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    @staticmethod
    def get_key_and_iv(password, salt, klen=32, ilen=16, msgdgst='md5'):
        '''
        Derive the key and the IV from the given password and salt.

        This is a niftier implementation than my direct transliteration of
        the C++ code although I modified to support different digests.

        CITATION: http://stackoverflow.com/questions/13907841/implement-openssl-aes-encryption-in-python

        @param password  The password to use as the seed.
        @param salt      The salt.
        @param klen      The key length.
        @param ilen      The initialization vector length.
        @param msgdgst   The message digest algorithm to use.
        '''
        # equivalent to:
        #   from hashlib import <mdi> as mdf
        #   from hashlib import md5 as mdf
        #   from hashlib import sha512 as mdf
        mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
        password = password.encode('ascii', 'ignore')  # convert to ASCII

        try:
            maxlen = klen + ilen
            keyiv = mdf(password + salt).digest()
            tmp = [keyiv]
            while len(tmp) < maxlen:
                tmp.append(mdf(tmp[-1] + password + salt).digest())
                keyiv += tmp[-1]  # append the last byte
            key = keyiv[:klen]
            iv = keyiv[klen:klen + ilen]
            return key, iv
        except UnicodeDecodeError:
            return None, None


class Ocean(object):
    """
    Ocean Integrated Project Manager.
    """
    _init_done = False
    _config = {}
    manifest = {}

    _subprocess_popen = staticmethod(subprocess_popen)

    def _decrypt(self, content):
        data = AESCipher(self._get_config("aes-key")).decrypt(bz2.decompress(content))
        return data

    def _check_signature_filename(self, mpath):
        if self._get_config("authority-pubkey"):
            public_key_data = open(self._get_config("authority-pubkey"), "rb").read()
            signature = open(re.sub(r'.(yaml|json)(".enc.bz2"?)',
                                    lambda g: ("." + g.group(1) + ".sig"),
                                    mpath
                                    ), "rb").read()
            pkey = load_publickey(FILETYPE_PEM, public_key_data)
            x509 = X509()
            x509.set_pubkey(pkey)
            assert verify(x509, signature, open(mpath, "rb").read(), 'sha256')

    def _read_manifest(self):
        """
        Read the manifest and integrates the system manifest in it.

        NOTE: two global variables omanifest and manifest are affected.

        :return: manifest
        """
        mpath = self.MANIFEST_PATH
        try:
            if self._get_config("direct-submanifest"):
                section, project = self._get_config("direct-submanifest").split(".")
                omanifest = {section: {
                    project: {
                        "alt-src": mpath
                    }
                }
                }
            elif mpath.startswith("docker:"):
                mpath = mpath[7:]
                omanifest = {"running": {}}
                for c in self._docker.containers():
                    if re.match(mpath, c["Names"][0].split('/')[-1]):
                        r = c.get("Labels", {}).items()
                        r = [(i[0][6:].lower().replace('_', '-'), json.loads(i[1])["@value"])
                             for i in r if i[0].startswith("OCEAN.")]
                        soft_update(omanifest["running"].setdefault(c["Names"][0].split('/')[-1], {}), dict(r))
            elif mpath.endswith("yaml.enc.bz2"):
                logging.info("Found crypto-signed YAML manifest")
                file_data = open(mpath, "rb").read()

                omanifest = self._decrypt(file_data)
            elif mpath.endswith("json.enc.bz2"):
                logging.info("Found crypto-signed JSON manifest")
                self._check_signature()
                file_data = open(mpath, "rb").read()
                data = AESCipher(self._get_config("aes-key")).decrypt(StringIO(bz2.decompress(file_data)))
                omanifest = json.loads(data)
            elif mpath.endswith("yaml"):
                omanifest = yaml.load(open(mpath, "r").read())
            else:
                omanifest = json.loads(open(mpath, "r").read())
        except BaseException:
            traceback.print_exc()
            logging.warning("manifest not found !")
            omanifest = {}
        omanifest = recupdate(omanifest, SYSTEM_MANIFEST)
        if os.path.exists(os.path.join(self.MP, "system.yaml")):
            manifest = recupdate(omanifest, yaml.load(open(os.path.join(MP, "system.yaml"), "r").read()))
        elif os.path.exists(os.path.join(self.MP, "system.json")):
            manifest = recupdate(omanifest, json.loads(open(os.path.join(MP, "system.json"), "r").read()))
        else:
            manifest = deepcopy(omanifest)
        self.manifest = manifest
        self.omanifest = omanifest
        if DEEP_MANIFEST:
            logging.debug("checking for submanifests")
            sections = list(self.manifest.keys())
            for k in sections:
                repos = list(self.manifest[k].keys())
                for s in repos:
                    srcp = self._get_srcp(s, k)

                    for p, dec in [
                        ("manifest.yaml.enc.bz2", lambda data: yaml.load(self._decrypt(data))),
                        ("manifest.json.enc.bz2", lambda data: json.loads(self._decrypt(data))),
                        ("manifest.yaml", yaml.load),
                        ("manifest.json", json.loads),

                    ]:
                        mp = os.path.join(srcp, "ocean", "manifest", p)
                        if os.path.exists(mp):
                            logging.debug("found submanifest :" + mp)
                            try:
                                soft_update(self.manifest[k],
                                            rec_rep(dec(open(mp).read()), "$SRVNAME$", s)
                                            )
                                break
                            except AttributeError:
                                continue
                            except Exception as exception:
                                traceback.print_exc()
                                logging.warning(mp + str(type(exception)) + ":" + str(exception))
                        else:
                            mp = os.path.join(srcp, p)
                            if os.path.exists(mp):
                                logging.debug("found submanifest :" + mp)
                                try:
                                    soft_update(self.manifest[k],
                                                rec_rep(dec(open(mp).read()), "$SRVNAME$", s)
                                                )
                                    break
                                except Exception:
                                    traceback.print_exc()
                                    logging.warning(mp + str(type(exception)) + ":" + str(exception))
        return self.manifest

    def nop(self):
        """Initialise Ocean and quit just after."""
        return True

    def env_info(self):
        """Information about current environment."""
        return dict(
            DOCKER_OPTS=os.environ.get("DOCKER_OPTS", ""),
            OCEAN_STORAGE=self._get_config("STORAGE", "/sto")
        )

    def _read_config(self):
        """Read user configuration file if it exists."""
        fn = os.path.expanduser("~/.ocean-config.yaml")
        if os.path.exists(fn):
            self._config.update(yaml.load(open(fn).read()))
        fn = os.path.expanduser("~/.ocean-config.json")
        if os.path.exists(fn):
            self._config.update(json.load(open(fn)))

    def _get_config(self, varname, default=None):
        """Read a value from config or env."""
        if xhasattr(self._config, varname):
            return xgetattr(self._config, varname)
        if ("OCEAN_" + varname.replace(".", "_").replace("-", "_").upper()) in os.environ:
            return os.environ[("OCEAN_" + varname.replace(".", "_").replace("-", "_").upper())]
        if varname in DEFAULT_CONFIG:
            return DEFAULT_CONFIG[varname]
        return default

    def _init(self):
        # READ CONFIGURATION
        self._docker = docker.Client(os.environ.get("DOCKER_HOST"))
        self._read_config()

        if self._get_config("debug", 0) != 0:
            rl = logging.getLogger()
            rl.setLevel(logging.DEBUG)

        self.dockerip = dockerip
        self._PIPELINE = []
        self._DOCKERENV_OPTIONS = []

        # LOAD MODULES
        for m in ALL_MIXINS:
            for a in dir(m):
                if not hasattr(self, a):
                    setattr(self, a, getattr(m, a))
            if hasattr(m, "_PIPELINE"):
                self._PIPELINE += m._PIPELINE
            if hasattr(m, "_dockerenv_options)"):
                self._DOCKERENV_OPTIONS.append(m._dockerenv_options)
            m._ocean = self

        for m in ALL_HANDLERS:
            for a in dir(m):
                if not hasattr(self, a) and not a[0] == "_" and not a.startswith("on_"):
                    setattr(self, a, getattr(m, a))

            if hasattr(m, "_PIPELINE"):
                self._PIPELINE += m._PIPELINE
            if hasattr(m, "_dockerenv_options)"):
                self._DOCKERENV_OPTIONS.append(m._dockerenv_options)

        self._PIPELINE = sorted(self._PIPELINE, key=lambda x: x[0])

        # FIXME: This is an option
        # if not os.path.exists(MANIFEST_PATH):
        #    os.system("git clone %s %s" % (MANIFEST_URL, MANIFEST_PATH))

        self.RepoManager = modules[self._get_config("repo_manager", "repo_gitlab")].RepoManager
        # self.IaaSClusterManager = modules[self._get_config("iaas_manager", "iass_dockermachine")].IaaSClusterManager

        self._read_manifest()

        for m in ALL_HANDLERS:
            if hasattr(m, "on_ocean_start"):
                m.on_ocean_start(self)

    def _container_name(self, n, nsrv=None):
        return OCEAN_NAME_PREFIX + n + ("" if nsrv is None else ("-" + nsrv))

    def _image_name(self, n, tagname=None):
        return self._container_name(n) + (":%s" % (tagname,) if tagname else "")

    def _src_folder(self, n):
        return n

    def _asrc_folder(self, section, srv):
        return os.path.join(SRC, section, self._src_folder(srv))

    def _cfg_folder(self, n):
        return (("atlantis/" + OCEAN_NAME_PREFIX + n) if OCEAN_NAME_PREFIX else n)

    def _require_name(self, n):
        """Format name for docker image identifiers."""
        return OCEAN_NAME_PREFIX + n

    def _docker_images(self, img_selector=lambda i: True):
        """
        Get details about docker images.
        """
        res = {}
        imgs = filter(img_selector, self._docker.images(all=True))
        for i in imgs:
            for t in i["RepoTags"]:
                res.setdefault(t.split(":")[0], []).append(i)
        return res

    def docker_clean_unused(self):
        """
        Find and remove unused docker images.

        (use at your own risk!)
        """
        os.system("docker images | awk '(/^<none>/){print $3;}'|xargs docker rmi")
        os.system("docker images -a -f \"dangling=true\" | awk '(/^<none>/){print $3;}'|xargs docker rmi -f")

    def dockerimg(self, srv):
        """Return the docker image used for a project."""
        section = self._find_section(srv)
        if "dockerimg" in self.manifest[section][srv]:
            return self.manifest[section][srv]["dockerimg"]
        else:
            return srv

    def _find_section(self, srv):
        """
        Find the section of a project in the self.manifest.
        """
        if "/" in srv:
            if len(srv.split("/")) != 2:
                logging.error("invalid number of components in service path")
            return srv.split("/")[0]

        for k in list(self.manifest.keys()):
            if srv in self.manifest[k]:
                return k
        raise Exception("Unknown service")

    def _last_predeploy(self):
        return [x[1] for x in self._PIPELINE if x[0] < 100][-1]

    def _last_predeploy_tag(self, version=None):
        if version is None:
            version = "latest"
        return self._last_predeploy() + "-" + version

    def _find_section_new(self, srv):
        """
        Find the section of a project in the self.manifest.
        """
        if ":" in srv:
            srv, tag = srv.split(":")
        else:
            tag = None

        if "/" in srv:
            if len(srv.split("/")) != 2:
                logging.error("invalid number of components in service path")
            s, ss, t = srv.split("/")[-2:], tag

        s = None
        for k in list(self.manifest.keys()):
            if srv in self.manifest[k]:
                s, ss, t = k, srv, tag
                break

        if s is None:
            raise Exception("Unknown service:" + srv)

        if "version" in self.manifest[s][ss]:
            t = self._last_predeploy_tag(version=self.manifest[s][ss]["version"])
        if t is None:
            t = self._last_predeploy_tag()
        return s, ss, t

    def clone(self, srv=None):
        """Clone sources for specific service."""
        if srv is None:
            for k in list(self.manifest.keys()):
                for s in self.manifest[k]:
                    self._call_with_eh("clone", k + "/" + s)
            return

        section, srv, tag = self._find_section_new(srv)

        if not os.path.exists(SRC):
            os.mkdir(SRC)
        if not os.path.exists(os.path.join(SRC, section)):
            os.mkdir(os.path.join(SRC, section))

        if "url" in self.manifest[section][srv]:
            srvp = self._get_srcp(srv, section)
            if os.path.exists(os.path.join(srvp, ".git")):
                logging.info("skipping" + srv)
                return

            _o, _e = subprocess_popen(
                "git clone --recursive %s %s" % (self.manifest[section][srv]["url"], self._src_folder(srv)), shell=True,
                cwd=os.path.join(SRC, section)).communicate()

            if "push_urls" in self._get(srv):
                for url in self._get(srv)["push_urls"]:
                    _o, _e = subprocess_popen("git remote set-url --add --push origin %s" % (url,),
                                              shell=True,
                                              cwd=self._get_srcp(srv, section)).communicate()
            if "version" in self._get(srv):
                _o, _e = subprocess_popen("git checkout tags/%s" % (
                    self._get(srv)["version"]), shell=True,
                    cwd=srvp).communicate()

    def pull(self, srv=None):
        """git pull source all services/a specific service."""
        if srv is None:
            for k in list(self.manifest.keys()):
                for s in self.manifest[k]:
                    self._call_with_eh("pull", k + "/" + s)
            return

        section, srv, tag = self._find_section_new(srv)

        if "url" in self._get(srv):
            assert (os.path.exists(SRC))
            srvp = self._get_srcp(srv, section)
            assert (os.path.exists(srvp))
            _o, _e = subprocess_popen("git pull", shell=True, cwd=srvp).communicate()

    def _legacy_fullyconnect(self, *srvs):
        """Deprecated - from docker 0.10.0 since DNS are now provided as standard network service."""
        r = self._docker_ps()
        hosts = """
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
        """.strip() + "\n"
        for x in r:
            if x[1].startswith("Exited"):
                continue
            o, e = subprocess_popen(
                "docker inspect --format '{{ .NetworkSettings.IPAddress }} {{ .Name }}' %s" % (x[0],), shell=True,
                stdout=subprocess.PIPE).communicate()
            if re.match("^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}) /([^ ]+)", o):
                hosts += o.replace('/', '')
        if len(srvs) == 0:
            srvs = []
            for s in self.manifest["services"]:
                if self.manifest["services"][s].get("fullyconnect", False):
                    srvs.append(s)
        ps = dict(r)
        for x in srvs:
            if (x not in ps) or ps[x].startswith("Exited"):
                continue
            subprocess_popen("docker exec -i %s /bin/sh -c \"cat > /etc/hosts\"" % (x,), shell=True,
                             stdin=subprocess.PIPE).communicate(hosts)
        return hosts

    def _alt_fullyconnect(self, *srvs):
        """
        Connect container together.

        We still use fully connect to provide a host file to the service
        that run on the host network and may want to access other containers.
        """
        r = self._docker_ps()
        hosts = open("/etc/hosts").read().strip() + "\n"
        for x in r:
            if x[1].startswith("Exited"):
                continue
            o, e = subprocess_popen(
                "docker inspect --format "
                "'{{.NetworkSettings.Networks.pacific.IPAddress}} {{ .Name }} {{ .Name }}.pacific' %s" % (x[0],),
                shell=True,
                stdout=subprocess.PIPE).communicate()
            o = o.decode('utf-8')
            if re.match("^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}) /([^ ]+)", o):
                hosts += o.replace('/', '')

        hosts = [x for x in [x.strip() for x in hosts.split("\n")] if len(x) and x[0] != "#"]
        hosts = [re.sub("([ \t]+)", " ", x).split(" ") for x in hosts]
        hosts_dict = {}
        for x in hosts:
            hosts_dict.setdefault(x[0], []).extend(x[1:])
        hosts = [" ".join([i[0]] + i[1]) for i in hosts_dict.items()]
        hosts = "\n".join(hosts)
        if os.path.exists(os.path.join(MPL, "hosts")):
            os.unlink(os.path.join(MPL, "hosts"))
        hosts = open(os.path.join(MPL, "hosts"), "wb").write(hosts.encode('utf8'))

    def get_ip(self, srv, strict=True):
        """
        Return the IP of a container.

        :param srv: Name of the project.
        :return: The IP of the container.
        """
        c = self._docker.inspect_container(srv)
        if not c:
            return ""
        if strict:
            r = c["NetworkSettings"]["Networks"]["pacific"]["IPAddress"]
        else:
            r = "%s %s %s.pacific" % (c["NetworkSettings"]["Networks"]["pacific"]["IPAddress"], c["Name"], c["Name"])
        return r.strip().split(' ')[0].strip().replace(':', '')

    def _get_cfgp(self, srv):
        """
        Return the path of folder holding specific configuration files for the container.
        """
        section = self._find_section(srv)
        if section.startswith("local-"):
            return os.path.join(CFGL, self._cfg_folder(srv))
        else:
            return os.path.join(CFG, self._cfg_folder(srv))

    def _get_srcp(self, srv, section=None):
        """
        Return the path of folder holding specific configuration files for the container.
        """
        if section is None:
            section = self._find_section(srv)

        if not (isinstance(self.manifest[section][srv], dict)):
            logging.warning("Invalid section : %s %s %r" % (section, srv, self.manifest[section][srv],))
            assert False
        srv = self.manifest[section][srv].get("alt-src", srv)

        return os.path.join(SRC, section, self._src_folder(srv))

    def _get(self, srv):
        return ocean__get(self, srv)

    def dockerenv_options(self, srv, nsrv=None, with_expose=False, joined=True, xtra=None, root=False):
        """
        Generate command line options for running a specic service.
        """
        if nsrv is None:
            nsrv = self._container_name(srv)

        if xtra is None:
            xtra = []

        section = self._find_section(srv)

        srvp = self._get_srcp(srv, section)
        cfgp = self._get_cfgp(srv)

        extraargs = self._get(srv).get("extraargs", []) + xtra
        r = []

        if root:
            extraargs = [e for e in extraargs if not e.startswith("-u ")]
            extraargs.append("-u 0")

        if "--net=host" not in extraargs:
            r.append("--net=%s" % (self.DEFAULT_NETWORK,))
            r.append("--net-alias=%s" % (nsrv + self.DEFAULT_DOMAIN,))
            for x in self._get(srv).get("requires", []):
                if self.is_started(x):
                    r.append("--link=%s:%s" % (self._require_name(x), x,))
        uid = os.environ.get("OCEAN_UID", str(os.getuid()))
        if not len(list(filter(lambda a: a.startswith("-u "), extraargs))):
            user = self._get(srv).get("user", self._get_config("user"))
            if user:
                user = user.replace("$UID$", uid)
                r.append("-u " + user)
                r.append("-v /etc/passwd:/etc/passwd")
                r.append("-v /etc/group:/etc/group")
            else:
                logging.info("No user specified. running as root.")
        else:
            logging.debug("User already specified via extraargs")

        r.append("--name=%s" % (nsrv,))

        if not OCEAN_NAME_PREFIX:
            if with_expose:
                for x in self._get(srv).get("expose", []):
                    r.append("-p %s" % (x,))

                    # if self._get(srv).get("user",False) is False:
                    # r.append("-u %d"%(os.getuid(),))
                    # else:
                    # r.append("-u %d"(self._get(srv)["user"]))

        for x in extraargs:
            r.append(x.replace("$OCEANPATH$", self.MP)
                     .replace("$OCEANIP$", dockerip)
                     .replace("$OCEANRANDOM$", OCEAN_RANDOM)
                     .replace("$UID$", uid)
                     .replace("$HOME$", os.path.expanduser("~")))

        if os.path.exists(srvp):
            r.append("-v %s:/home/%s/src" % (srvp, srv))
            r.append("-v ~/.ssh:/home/%s/.ssh" % (srv,))
            r.append("-v ~/.ssh:/root/.ssh")
            r.append("-e HOME=/home/%s" % (srv,))
            r.append("-w /home/%s/src" % (srv,))

        if os.path.exists(cfgp):
            for f in list(self._get(srv).get("config-files", {}).items()):
                if f[0][-1] == '*':
                    f = (f[0][:-1], f[1])
                sn = f[0].replace('/', '_').replace(".", "_")
                if f[0][0] == '/':
                    r.append("-v %s/%s:%s:ro" % (cfgp, sn, f[0]))
                else:
                    r.append("-v %s/%s" % (cfgp, sn) + ":" + os.path.abspath("/home/%s/src/%s" % (srv, f[0]))) + ":ro"

        if os.path.exists(os.path.join(cfgp, "key")):
            r.append("-v %s/key:/.key.pem" % (cfgp,))
        if os.path.exists(os.path.join(cfgp, "cert")):
            r.append("-v %s/cert:/.cert.pem" % (cfgp,))
        if os.path.exists(os.path.join(cfgp, "cacert")):
            r.append("-v %s/cacert:/.cacert.pem" % (cfgp,))

        r.append("-h %s" % (nsrv,))

        for dof in self._DOCKERENV_OPTIONS:
            r = dof(section, srv, r)

        if joined:
            return " ".join(r)
        else:
            return r

    def status(self, srv=None, *options):
        """
        Indicate the status of the different elements of a project.
        """
        if srv is None or srv == "-a":
            for k in list(self.manifest.keys()):
                for s in self.manifest[k]:
                    self.status(s)
            return
        print(srv, ("on" if self.is_started(srv) else "off"))

    def kill(self, srv=None, *options):
        """
        Stop one or many container.
        """
        if srv is None or srv == "-a":
            for k in list(self.manifest.keys()):
                for s in self.manifest[k]:
                    self.kill(s)
            return True
        if self.is_started(srv):
            o, e = subprocess_popen("docker kill %s" % (self._container_name(srv)), shell=True).communicate()
        return True

    def rm(self, srv=None, *options):
        """Remove a container."""
        o, e = subprocess_popen("docker rm %s" % (self._container_name(srv)), shell=True).communicate()

    def _update_config(self, srv=None):
        if srv is None or srv == "-a":
            for k in list(self.manifest.keys()):
                for s in self.manifest[k]:
                    self._update_config(s)
            return
        if not os.path.exists(CFG):
            os.mkdir(CFG)
        section = self._find_section(srv)
        srvp = os.path.join(SRC, section, self._src_folder(srv))
        cfgp = self._get_cfgp(srv)

        if not os.path.exists(srvp) and ("config-files" not in self._get(srv)):
            if "with_ssl" not in self._get(srv):
                return

        if not os.path.exists(cfgp):
            if not os.path.exists(os.path.dirname(cfgp)):
                os.mkdir(os.path.dirname(cfgp))
            os.mkdir(cfgp)

        for f in list(self._get(srv).get("config-files", {}).items()):
            executable = False
            if f[0][-1] == '*':
                f = (f[0][:-1], f[1])
                executable = True
            sn = f[0].replace('/', '_').replace(".", "_")
            cf = open(os.path.join(cfgp, sn), "wb")
            cf.write((f[1].replace('$hostip$', dockerip)).encode('utf8'))
            cf.close()
            if executable:
                os.chmod(os.path.join(cfgp, sn), 0o711)

        if not os.path.exists(srvp):
            if "with_ssl" not in self._get(srv):
                return

        if self._get(srv).get("with_ssl", False):
            if not os.path.exists(os.path.join(cfgp, "cert")):
                self.generate_ssl_keys(srv)
                if os.path.exists(os.path.join(cfgp, "cacert")):
                    os.unlink(os.path.join(cfgp, "cacert"))
                shutil.copy2(os.path.join(cfgp, "..", "..", ".virtca/intermediate/certs/", "ca-chain.cert.pem"),
                             os.path.join(cfgp, "cacert"))
                if os.path.exists(os.path.join(cfgp, "cert")):
                    os.unlink(os.path.join(cfgp, "cert"))
                shutil.copy2(os.path.join(cfgp, "..", "..", ".virtca/intermediate/certs/", "%s.cert.pem" % (srv,)),
                             os.path.join(cfgp, "cert"))
                if os.path.exists(os.path.join(cfgp, "key")):
                    os.unlink(os.path.join(cfgp, "key"))
                shutil.copy2(os.path.join(cfgp, "..", "..", ".virtca/intermediate/private/", "%s.key.pem" % (srv,)),
                             os.path.join(cfgp, "key"))

    def generate_ssl_keys(self, srv):
        """Generate SSL keys if needed."""
        vca = "CABASEDIR=%s python %s/modules/vca.py -i " % (
            os.path.abspath(os.path.join(self._get_cfgp(srv), "..", "..")), AP)
        cmd = vca + " " + srv
        _o, _e = subprocess_popen(cmd, shell=True).communicate()

    def shell(self, srv, *options, **kwargs):
        """
        Start a shell in a new container for a specific image.

        NOTE: this is a new container: different from docker exec!
        """
        command = kwargs.get("command", "/bin/bash")
        xtraargs = kwargs.get("xtraargs", [])
        transform = kwargs.get("transform", lambda x: x)
        verbose = False
        section, srv, tag = self._find_section_new(srv)
        nsrv = self._container_name(srv)
        mode = TI
        rm = "--rm"

        if "-c" in options:
            command = ' '.join(["'%s'" % (_o,) for _o in options[(options.index("-c") + 1):]])  # FIXME: needs escaping
            options = options[:(options.index("-c") + 1)]

        if "-la" in options:
            xtraargs.append("%s" % (
                " ".join(
                    [" --link=%s:%s" % (x, x,) for x in list(self.manifest[section].keys()) if (self.is_started(x))]),))
        if "-n" in options:
            n = options[options.index("-n") + 1]
            nsrv = srv + "-" + n
        if "-v" in options:
            verbose = True
        if "-p" in options:
            mode = "-i"
        if "-d" in options:
            mode = "-d"
            rm = ""
        if "-k" in options:
            rm = ""

        for oi, ov in enumerate(options):
            if ov == '-e':
                xtraargs.append("-e " + options[oi + 1])  # FIXME: obviously week -e -e
        for oi, ov in enumerate(options):
            if ov == '-V':
                xtraargs.append("-v " + options[oi + 1])  # FIXME: obviously week -V -V

        # ensure the image is built and ready to run
        if not self.is_built(srv, tag):
            r = self.build(srv, tag=tag)
            if not r:
                logging.warning("Failed to build : " + srv + ":" + tag)
                return False, -1

        if self.is_started(nsrv):
            logging.warning("Already started : " + nsrv)
            return False, -1

        self.free_if_exited(nsrv)
        self._update_config(srv)

        # run the command
        cmd = "%s run %s %s -P %s %s %s" % (
            ("nvidia-docker" if self._get(srv).get("use-nvidia-docker") else self._get_config("docker-cmd")),
            rm, mode, transform(self.dockerenv_options(srv, nsrv, xtra=xtraargs)),
            self._image_name(srv, tag),
            command)
        if verbose:
            logging.info(cmd)
        p = subprocess_popen(cmd, shell=True)
        o, e = p.communicate()
        return p.returncode == 0, p.returncode

    def exec_(self, srv, *options, **kwargs):
        """
        Docker exec with specifed container.
        """
        command = kwargs.get("command", "/bin/bash")
        nsrv = self._container_name(srv)
        verbose = False
        section, srvs, tag = self._find_section_new(srv)
        mode = TI

        if "-c" in options:
            command = ' '.join(["'%s'" % (_o,) for _o in options[(options.index("-c") + 1):]])  # FIXME: needs escaping
            options = options[:(options.index("-c") + 1)]
        if "-n" in options:
            n = options[options.index("-n") + 1]
            nsrv = srv + "-" + n
        if "-v" in options:
            verbose = True
        if "-p" in options:
            mode = "-i"

        cmd = "docker exec %s %s %s" % (mode, nsrv, command)
        if verbose:
            logging.info(cmd)
        p = subprocess_popen(cmd, shell=True)
        o, e = p.communicate()
        return p.returncode == 0, p.returncode

    def _docker_ps(self):
        """
        List running containers.
        """
        o, _e = subprocess_popen("docker ps -a", shell=True, stdout=subprocess.PIPE).communicate()
        ol = o.split(b"\n")
        ol0 = ol[0]
        stb = ol0.index(b"STATUS")
        nmb = ol0.index(b"NAMES")
        o = list(filter(len, ol))[1:]
        o = [(l[nmb:].strip().decode('utf8'), l[stb:(stb + 20)].strip().decode('utf8')) for l in o]
        return o

    def _docker_ps_new(self, *args, **kwargs):
        """
        List running containers.
        """
        res = {}
        for c in self._docker.containers(*args, **kwargs):
            res[c["Names"][0].split('/')[-1]] = c["Status"]
        return res

    def is_started(self, srv):
        """
        Indicate if a container ip up and started.

        :param srv: name of the project
        :return: indicate if the container is started.
        """
        s = self._docker_ps_new().get(self._container_name(srv), "exited").lower()
        return s.startswith("up ")

    def is_existing(self, srv):
        """
        Indicate if a container ip up and started.

        :param srv: name of the project
        :return: indicate if the container is started.
        """
        s = self._docker_ps_new(all=True).get(self._container_name(srv), "NA")
        return s != "NA"

    def is_exited(self, srv):
        """
        Indicate if a container has exited.

        :param srv: name of the project
        :return: indicate if the container is exited
        """
        status = dict(self._docker_ps()).get(self._container_name(srv), "nothere").lower()
        return status.startswith("exited") or status.startswith("dead") or status.startswith("created")

    def free_if_exited(self, srv):
        """
        Remove a previously existing container so that a new container can be started.

        :param srv: name of the project
        :return: indicate if the container is exited
        """
        if self.is_exited(srv):
            subprocess_popen("docker rm " + self._container_name(srv), shell=True, stdout=subprocess.PIPE).communicate()

    def free(self, srv):
        """
        Remove a previously existing container so that a new container can be started.

        :param srv: name of the project
        :return: indicate if the container is exited
        """
        subprocess_popen("docker rm -f " + self._container_name(srv), shell=True, stdout=subprocess.PIPE).communicate()

    def start(self, srv, *options, **kwargs):
        """
        Start a container and its dependencies.

        Extra options:

        -v : verbose mode
        -sr : skip required
        -SR : skip required and build
        -n name : container suffix (if you need multiple instances)
        """
        logging.debug("starting '%s'" % (srv,))

        allow_fail = False
        verbose = False
        skip_required = False
        skip_build = False
        remove_existing = False
        also_already_running = False
        only_requirements = False
        nsrv = srv

        if srv is None or srv == "-a":
            for k in list(self.manifest.keys()):
                for s in self.manifest[k]:
                    try:
                        self._call_with_eh("start", s, *options)
                    except Exception as e:
                        logging.warning(str(e))

            return

        logging.info(srv)
        section, ssrv, tag = self._find_section_new(srv)

        if "-sr" in options:
            skip_required = True
        if "-SR" in options:
            skip_required = True
            skip_build = True
        if "-v" in options:
            verbose = True
        if "-f" in options:
            allow_fail = True
        if "-or" in options:
            only_requirements = True
        if "-re" in options:
            remove_existing = True
            also_already_running = False
        if "-RE" in options:
            remove_existing = True
            also_already_running = True
        if "-n" in options:
            n = options[options.index("-n") + 1]
            nsrv = srv + "-" + n

        if not skip_build:
            if not self.is_built(srv):
                r = self._call_with_eh("build", srv)
                if not r:
                    return False

        logging.info(
            "status: srv%r , remove_existing:%r is_existing:%r" % (nsrv, remove_existing, self.is_existing(nsrv)))
        if remove_existing and self.is_existing(nsrv):
            logging.info("Already existing:" + nsrv)
            if (not also_already_running) and self.is_started(nsrv):
                logging.info("Already started:" + nsrv)
                return False
            self.free(nsrv)
        elif self.is_started(nsrv):
            logging.info("Already started:" + nsrv)
            return False
        else:
            self.free_if_exited(nsrv)

        srvp = self._get_srcp(srv)

        if not os.path.exists(srvp):
            self._call_with_eh("clone", srv)

        if "requires" in self._get(srv) and not skip_required:
            for ss in self._get(srv)["requires"]:
                try:
                    self._call_with_eh("start", ss, *options)
                except AssertionError:
                    if self._get(srv).get("soft-requirements", False):
                        logging.warning("Failed to start " + ss)
                    else:
                        raise

        if only_requirements:
            return

        self._update_config(srv)
        if not skip_build:
            self.register_service(srv, "-sr")

        if "pre-start" in self._get(srv):
            os.system(self._get(srv)["pre-start"])

        if self._get(srv).get("no_run"):
            return

        command = kwargs.get("command", self._get(srv).get("command", ""))

        if '&&' in command or '||' in command and not re.match("/bin/(\w*)?sh -c (.*)", command):
            command = "/bin/sh -c '%s'" % (command,)

        cmd = "%s run -d %s %s %s" % (
            ("nvidia-docker" if self._get(srv).get("use-nvidia-docker") else self._get_config("docker-cmd")),
            self.dockerenv_options(srv, self._container_name(nsrv), with_expose=True, xtra=kwargs.get("extraargs")),
            self._image_name(srv, tag),
            command
        )

        if verbose:
            logging.info(cmd)

        p = subprocess_popen(cmd, shell=True)
        o, e = p.communicate()

        assert allow_fail or (p.returncode == 0)

        time.sleep(0.1)
        if not allow_fail:
            assert (self.is_started(srv)), "%s failed to start and allow fail not set to True" % (srv)
        if hasattr(self, "browser"):
            self.browser(srv)

        logging.debug("started " + srv)
        return True

    def restart(self, srv, *options):
        """
        Restart a container.
        """
        if self.is_started(srv):
            if not self._call_with_eh("kill", srv):
                logging.warning("failed to stop " + srv)
                return
        return self._call_with_eh("start", srv)

    def hardreset(self, srv="-a"):
        """
        Reset all stratic data and restart entirely all the containers of all project.

        Remove all configuration files, and restart services.
        Data stored in the configuration folder will also be deleted.
        """
        if srv == "-a":
            self._call_with_eh("kill")
            o, e = subprocess_popen("sudo rm -rf cfg/ .certs/ .virtca/", shell=True, cwd=self.MP).communicate()
        else:
            self._call_with_eh("kill", srv)
            o, e = subprocess_popen("sudo rm -rf cfg/%s/registered cfg/%s/data" % (srv, srv), shell=True,
                                    cwd=self.MP).communicate()
            self._call_with_eh("start", srv)

    def path_info(self):
        """
        Return information about path used by ocean.
        """
        print("SRC", SRC)
        print("CFG", CFG)
        print("CFGL", CFGL)

    def ps(self):
        """
        List all containers running on current system.
        """
        os.system("docker ps")

    def logs(self, *options):
        """
        Return the logs of a specific container.
        """
        os.system("docker logs " + " ".join(list(options[:-1]) + [self._container_name(options[-1])]))

    def help(self, *options):
        """
        Describe possible ocean CLI commands.
        """
        r = "\n"
        r += "ocean <command> [args...] where command is one of:\n"
        r += "\n"
        for m in dir(self):
            if m[0] != "_" and callable(getattr(self, m)):
                r += ("-" + m + "\n")
                r += ("\n".join(
                    textwrap.wrap(textwrap.dedent(getattr(self, m).__doc__ or "undocumented!").strip(),
                                  60, initial_indent=" " * 8, subsequent_indent=" " * 8)
                ) + "\n")
        r += ("\n")
        print (r)

    def _call_with_eh(self, mn, *argv, **kwargs):
        """Call event handlers associated with a method."""
        for m in ALL_HANDLERS:
            if hasattr(m, "on_pre_" + mn):
                getattr(m, "on_pre_" + mn)(*argv, **kwargs)

        r = getattr(self, mn)(*argv, **kwargs)

        for m in ALL_HANDLERS:
            if hasattr(m, "on_post_" + mn):
                getattr(m, "on_post_" + mn)(*argv, **kwargs)

        return r

    def describe(self, srv, *options):
        """Return sections of the manifest that are related to a specific service."""
        section = self._find_section(srv)
        if "-y" in options:
            return "%s/%s\n%s\n" % (section, srv, yaml.dump(self._get(srv)),)
        else:
            return "%s/%s\n%s\n" % (section, srv, json.dumps(self._get(srv), indent=2),)

    def _all_services(self):
        """Enumerate all the services present in the manifest and their section."""
        for k in list(self.manifest.keys()):
            for srv in self.manifest[k]:
                yield k, srv

    def submanifest(self, srv, manifest=None, raw=False):
        """ Output a manifest that contains only a specific service and its dependencies."""
        rmanifest = manifest or {}
        section, srv, tag = self._find_section_new(srv)
        if rmanifest.setdefault(section, {}).get(srv, None):
            return rmanifest
        rmanifest[section][srv] = self.manifest[section][srv]
        for x in rmanifest[section][srv].get("requires", []):
            try:
                rmanifest = self.submanifest(x, rmanifest)
            except Exception:
                traceback.print_exc()
        if raw:
            return rmanifest
        else:

            return yaml.dump(rmanifest)

    def submanifest_hash(self, srv):
        return hashlib.md5(json.dumps(self.submanifest(srv)).encode('utf-8')).hexdigest()


default_ocean = None


def get_ocean(force=False, **kwargs):
    global default_ocean
    if (not default_ocean) or force:
        default_ocean = Ocean()
        default_ocean.DEFAULT_NETWORK = "pacific"
        default_ocean.DEFAULT_DOMAIN = ".pacific"
        default_ocean.AP = AP
        default_ocean.MP = MP
        default_ocean.MPL = MPL
        default_ocean.SRC = SRC
        default_ocean.CFG = CFG
        default_ocean.CFGL = CFGL
        for k, v in kwargs.items():
            setattr(default_ocean, k, v)
            logging.info(k)

        if os.path.exists(os.path.join(default_ocean.MP, "manifest")):
            MANIFEST_PATH = os.environ.get("OCEAN_MANIFEST", os.path.join(default_ocean.MP, "manifest"))
        else:
            MANIFEST_PATH = os.environ.get("OCEAN_MANIFEST", default_ocean.MP)
        assert (len(MANIFEST_PATH))

        if os.path.isdir(MANIFEST_PATH):
            if os.path.exists(os.path.join(MANIFEST_PATH, "manifest.yaml")):
                MANIFEST_PATH = os.path.join(MANIFEST_PATH, "manifest.yaml")
            if os.path.exists(os.path.join(MANIFEST_PATH, "manifest.json")):
                MANIFEST_PATH = os.path.join(MANIFEST_PATH, "manifest.json")

        logging.info("MANIFEST_PATH=" + MANIFEST_PATH)
        default_ocean.MANIFEST_PATH = MANIFEST_PATH

        default_ocean.process_run = subprocess_popen
        default_ocean._init()
        default_ocean._init_done = True

    return default_ocean


def main(argv=None, *args, **kwargs):
    """
    Main program manages access to ocean procedures.
    """
    if argv is None:
        argv = sys.argv[1:]

    ocean = get_ocean(*args, **kwargs)

    if len(argv) == 0 or not hasattr(ocean, argv[0]):
        ocean.help()
        sys.exit(-1)

    r = ocean._call_with_eh(argv[0], *argv[1:])

    if argv[0] in ["shell", "exec_", "tdd", "bdd", "unit", "bdd_spec"]:
        sys.exit(r[1])
    else:
        print(r)


if __name__ == "__main__":
    main()
