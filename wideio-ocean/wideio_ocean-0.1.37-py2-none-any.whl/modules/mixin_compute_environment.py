import json
import logging
import subprocess

# import paramiko


class MixIn(object):
    """
    MixIn to allow to run program in dev mode.

    Characteristics of dev mode are :
    - connected with databases and other requrired services...
    - ability to run editor/debugger with UI from the container (hence host network ?)
    """

    @classmethod
    def _proxy_ssh(cls, hosts, identity, command, input=None):
        for host in hosts:
            logging.debug(" ".join(["ssh", "-l", identity, host, command]))
            p = subprocess.Popen(["ssh", "-l", identity, host, command], stdin=subprocess.PIPE)
            o, e = p.communicate(input)
            res = p.returncode
            if res == 0:
                break

        assert res == 0

    @classmethod
    def ce_push(cls, srv, *options, **kwargs):
        """
        Ensures the definition of the environment is matching local definition.
        """
        srvd = cls._ocean._get(srv)

        cls._proxy_ssh(srvd["ce-proxies"], srvd["ce-user"],
                       "test -d ocean/manifest || mkdir -p ocean/manifest; cat > ocean/manifest/manifest.json",
                       input=json.dumps(cls._ocean.freeze(srv)))

    @classmethod
    def ce_freeze(cls, srv, *options, **kwargs):
        """
        Obtain a copy of the current environment
        """
        srvd = cls._ocean._get(srv)
        cls._proxy_ssh(srvd["ce-proxies"], srvd["ce-user"],
                       "OCEAN_PATH=~/ocean OCEAN_MANIFEST=~/ocean/manifest/manifest.json"
                       " DOCKER_HOST=%s ocean freeze %s" % (srvd["ce-docker"],
                                                            srv,))

    @classmethod
    def ce_start(cls, srv, *options, **kwargs):
        """
        Calls a remote proxy node to start the compute environment.
        """
        srvd = cls._ocean._get(srv)
        srchash = cls._ocean.freeze_hash(srv)
        assert (srvd["type"] == "environment")
        cls._proxy_ssh(srvd["ce-proxies"], srvd["ce-user"], "DOCKER_HOST=%s ocean start %s"
                       % (srvd["ce-docker"],
                          srv,)
                       )
        cls._proxy_ssh(srvd["ce-proxies"], srvd["ce-user"],
                       "OCEAN_CKSUM=%s OCEAN_PATH=~/ocean OCEAN_MANIFEST=~/ocean/manifest/manifest.json"
                       " DOCKER_HOST=%s ocean restart nginx" % (
                           srchash,
                           srvd["ce-docker"],
        ))

    @classmethod
    def ce_kill(cls, srv, *options, **kwargs):
        """
        Calls a remote proxy node to start the compute environment.
        """
        srvd = cls._ocean._get(srv)
        srchash = cls._ocean.freeze_hash(srv)
        assert (srvd["type"] == "environment")

        cls._proxy_ssh(srvd["ce-proxies"], srvd["ce-user"],
                       "OCEAN_CKSUM=%s OCEAN_PATH=~/ocean OCEAN_MANIFEST=~/ocean/manifest/manifest.json"
                       " DOCKER_HOST=%s ocean kill %s" % (
                           srchash,
                           srvd["ce-docker"],
                           srv,))

    @classmethod
    def ce_status(cls, srv, *options, **kwargs):
        """
        Calls a remote proxy node to start the compute environment.
        """
        srvd = cls._ocean._get(srv)
        srchash = cls._ocean.freeze_hash(srv)
        assert (srvd["type"] == "environment")

        cls._proxy_ssh(srvd["ce-proxies"], srvd["ce-user"],
                       "OCEAN_CKSUM=%s OCEAN_PATH=~/ocean OCEAN_MANIFEST=~/ocean/manifest/manifest.json"
                       " DOCKER_HOST=%s ocean start %s" % (
                           srchash,
                           srvd["ce-docker"], srv,))

    @classmethod
    def ce_build(cls, srv, *options, **kwargs):
        """
        Build containers that need to be build locally, and upload them so that they can be started later on.

        USERNAME and PASSWORD for the push have to be provided by the environment or the commandline.
        """
        srvd = cls._ocean._get(srv)
        # srchash = cls._ocean.freeze_hash(srv)
        assert (srvd["type"] == "environment")

        cls._ocean.build(srv, "-R", *options, **kwargs)

        # cls._proxy_ssh(srvd["ce-proxies"], srvd["ce-user"],
        #                       "OCEAN_CKSUM=%s OCEAN_PATH=~/ocean OCEAN_MANIFEST=~/ocean/manifest/manifest.json"
        #               " DOCKER_HOST=%s ocean build %s" % (
        #                   srchash,
        #                   srvd["ce-docker"],
        #                   srv,)
        #               )
