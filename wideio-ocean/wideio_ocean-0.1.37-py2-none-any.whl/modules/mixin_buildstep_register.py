import logging
import os


class MixIn(object):

    """
    Register is a step that is designed for a container to register with its environment.

    It should be applied AFTER deployment.
    Hence, in Ocean deployment is pipeline step greater than 100.
    """

    _PIPELINE = [
        (110, "registered")
    ]

    @classmethod
    def _pipeline_prev(cls):
        """
        Identify the previous build step in the build pipeline.
        """
        return cls._ocean._PIPELINE[cls._ocean._PIPELINE.index(cls._PIPELINE[-1]) - 1][1]

    @classmethod
    def _do_build_registered(cls, srv=None, *options, **kwargs):
        """
        Register a service in current swarm environment.

        We need to clarify is it par of externalf build pipeline ? / part of external pipeline ?...
        """
        logging.debug("Actually building '%s' to stage 'registered'" % (srv,))
        section, srv, tag = cls._ocean._find_section_new(srv)

        cfgp = cls._ocean._get_cfgp(srv)
        # srvp = cls._ocean._get_srcp(srv)
        force = False
        skiprequired = False

        if cls._ocean.is_started(srv + "-registration"):
            logging.error("Can't update while running")
            return False

        if cls._ocean.is_exited(srv + "-registration"):
            cmd = "docker rm %s" % (cls._ocean._container_name(srv + "-registration"),)
            o, e = cls._ocean._subprocess_popen(cmd, shell=True).communicate()

        if "-f" in options:
            force = True
        if "-sr" in options:
            skiprequired = True

        need_register = ((not os.path.exists(os.path.join(cfgp, "registered"))) or force) and (
            "register-cmd" in cls._ocean._get(srv, False))

        if need_register:
            logging.debug("Registration needed - starting service and proceeding to registration")
            if "requires" in cls._ocean._get(srv, False) and not skiprequired:
                for ss in cls._ocean._get(srv, False)["requires"]:
                    if not cls._ocean.is_started(ss):
                        r = cls._ocean._call_with_eh("start", ss)
                        if not r:
                            logging.warning("Failed to start service required for register step")
                            return r

            if not cls._ocean._call_with_eh("shell", srv + ":" + cls._pipeline_prev() + "-latest", "-n",
                                            "registration", "-v",
                                            command=cls._ocean._get(srv, False)["register-cmd"],
                                            # logs=os.path.join(cls._ocean.MPL,"logs", src+"@"+"register"+".log" )
                                            )[0]:
                logging.warning("Registration failed :" + srv)
                return False

            open(os.path.join(cfgp, "registered"), "wb").write("")

        else:
            logging.debug("No registration needed - simply adding tag")
            os.system("docker tag %s %s" % (cls._ocean._image_name(srv, cls._pipeline_prev() + "-latest"),
                                            cls._ocean._image_name(srv, "registered-latest")))

        return True

    @classmethod
    def register_service(cls, srv=None, *options):
        """
        Use this function is to be used to connect a container to its environment.

        This function implements the last step to transform the generic environment indicated by
        the dockerimg or dockerfile into the correct environment for the source code.
        """
        logging.debug("Called register_service `%s`" % (srv,))
        if srv is None or srv == "-a":
            for k in list(cls._ocean.manifest.keys()):
                for s in cls._ocean.manifest[k]:
                    cls.register_service(s, options)
            return

        cls._ocean._call_with_eh("build", srv, options, tag="registered")
