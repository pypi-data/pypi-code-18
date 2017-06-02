import logging
import os
import shutil
import uuid


class MixIn(object):
    """
    Update an image so that it includes depencies requireed by code.
    """

    _PIPELINE = [
        (50, "built")
    ]

    @classmethod
    def _pipeline_prev(cls):
        """
        Identify the previous build step in the build pipeline.
        """
        return cls._ocean._PIPELINE[cls._ocean._PIPELINE.index(cls._PIPELINE[-1]) - 1][1]

    @classmethod
    def _do_build_built(cls, srv=None, *options, **kwargs):
        """
        Update an image so that it includes depencies requireed by code.

        This function implements the last step to transform the generic environment indicated by
        the dockerimg or dockerfile into the correct environment for the source code.
        """
        section, ssrv, tag = cls._ocean._find_section_new(srv)

        if "-f" not in options:
            if cls._ocean.cache_try_pull_image(srv, cls._PIPELINE[0][1] + "-" + cls._ocean.manifest[section][ssrv].get(
                    "version", "latest")):
                return True

        srvp = cls._ocean._get_srcp(srv)

        # FIXME This should be true for the build container or we need build ids
        # if cls._ocean.is_started(srv):
        #    logging.error("can't update while running")
        #    return False

        if cls._ocean.is_exited(srv):
            o, e = cls._ocean._subprocess_popen("docker rm %s" % (cls._ocean._container_name(srv, nsrv="xreqblt"),),
                                                shell=True).communicate()

        cfgp = cls._ocean._get_cfgp(srv)
        l1 = set()
        if os.path.exists(cfgp):
            l1 = set(os.listdir(cfgp))

        done = False

        if cls._ocean._get(srv).get("build-cmd") or cls._ocean._get(srv).get("build-cmd-root"):
            prev = cls._ocean._image_name(srv, cls._pipeline_prev() + "-" + cls._ocean.manifest[section][ssrv].get(
                "version", "latest"))
            if cls._ocean._get(srv).get("build-cmd-root", False):
                logging.debug("running build-cmd-root")
                tmpid = str(uuid.uuid4())[:8]
                cmd = "docker run %s %s %s" % (
                    cls._ocean.dockerenv_options(srv,
                                                 nsrv=cls._ocean._container_name(srv, nsrv="xreqblt") + tmpid,
                                                 root=True),
                    prev,
                    cls._ocean._get(srv)["build-cmd-root"]
                )
                logging.debug(cmd)
                _o, _e = cls._ocean._subprocess_popen(cmd, shell=True).communicate()
                cmd = "docker commit %s %s" % (cls._ocean._container_name(srv, nsrv="xreqblt") + tmpid,
                                               cls._ocean._image_name(srv, cls._PIPELINE[0][1] + "-interm"))
                logging.debug(cmd)
                _o, _e = cls._ocean._subprocess_popen(cmd,
                                                      shell=True).communicate()
                prev = cls._ocean._image_name(srv, cls._PIPELINE[0][1] + "-interm")
            else:
                pass

            if cls._ocean._get(srv).get("build-cmd"):
                logging.debug("running build-cmd")
                tmpid = str(uuid.uuid4())[:8]
                cmd = "docker run %s %s %s" % (
                    cls._ocean.dockerenv_options(srv,
                                                 nsrv=cls._ocean._container_name(srv, nsrv="xreqblt") + tmpid),
                    prev,
                    cls._ocean._get(srv)["build-cmd"]
                )
                logging.debug(cmd)
                _o, _e = cls._ocean._subprocess_popen(cmd, shell=True).communicate()
                cmd = "docker commit %s %s" % (cls._ocean._container_name(srv, nsrv="xreqblt") + tmpid,
                                               cls._ocean._image_name(srv, cls._PIPELINE[0][1] + "-" +
                                                                      cls._ocean.manifest[section][ssrv].get(
                                                                          "version", "latest")))
                logging.debug(cmd)
                _o, _e = cls._ocean._subprocess_popen(cmd,
                                                      shell=True).communicate()
            else:
                _o, _e = cls._ocean._subprocess_popen("docker tag %s %s" % (prev,
                                                                            cls._ocean._image_name(srv,
                                                                                                   cls._PIPELINE[0][
                                                                                                       1] + "-" +
                                                                                                   cls._ocean.manifest[
                                                                                                       section][
                                                                                                       ssrv].get(
                                                                                                       "version",
                                                                                                       "latest"))),
                                                      shell=True).communicate()

            done = True

        if not done:
            if os.path.exists(os.path.join(srvp, "ocean-build.sh")):
                logging.debug("running build-cmd")
                cmd = "docker run %s %s ./ocean-build.sh" % (
                    cls._ocean.dockerenv_options(srv, nsrv=cls._ocean._container_name(srv)),
                    cls._ocean._image_name(srv, cls._pipeline_prev() + "-" + cls._ocean.manifest[section][ssrv].get(
                        "version", "latest"))
                )
                logging.debug(cmd)
                _o, _e = cls._ocean._subprocess_popen(cmd, shell=True).communicate()
                cmd = "docker commit %s %s" % (cls._ocean._container_name(srv),
                                               cls._ocean._image_name(srv, cls._PIPELINE[0][1] + "-" +
                                                                      cls._ocean.manifest[section][ssrv].get(
                                                                          "version", "latest")))
                logging.debug(cmd)
                _o, _e = cls._ocean._subprocess_popen(cmd,
                                                      shell=True).communicate()
                done = True

        if not done:
            for p in ["requirements.txt", "requirements/dev.txt"]:
                if os.path.exists(os.path.join(srvp, p)):
                    cmd = "docker run %s %s pip install --upgrade -r %s" % (
                        cls._ocean.dockerenv_options(srv, nsrv=cls._ocean._container_name(srv)),
                        cls._ocean._image_name(srv, cls._pipeline_prev() + "-" + cls._ocean.manifest[section][ssrv].get(
                            "version", "latest")), p)
                    logging.debug(cmd)
                    _o, _e = cls._ocean._subprocess_popen(cmd, shell=True).communicate()
                    _o, _e = cls._ocean._subprocess_popen("docker commit %s %s" % (cls._ocean._container_name(srv),
                                                                                   cls._ocean._image_name(srv,
                                                                                                          cls._PIPELINE[
                                                                                                              0][
                                                                                                              1] + "-" +
                                                                                                          cls._ocean.manifest[
                                                                                                              section][
                                                                                                              ssrv].get(
                                                                                                              "version",
                                                                                                              "latest"))
                                                                                   ),
                                                          shell=True).communicate()
                    done = True
                    break

        if not done:
            _o, _e = cls._ocean._subprocess_popen(
                "docker tag %s %s" % (
                    cls._ocean._image_name(srv, cls._pipeline_prev() + "-" + cls._ocean.manifest[section][ssrv].get(
                        "version", "latest")),
                    cls._ocean._image_name(srv, cls._PIPELINE[0][1] + "-" + cls._ocean.manifest[section][ssrv].get(
                        "version", "latest"))),
                shell=True).communicate()

        # cleanup
        l2 = set()
        if os.path.exists(cfgp):
            l2 = set(os.listdir(cfgp))

        for x in l2 - l1:
            if os.path.isdir(os.path.join(cfgp, x)):
                shutil.rmtree(os.path.join(cfgp, x))

        cls._ocean.cache_push_image(srv, "built-" + cls._ocean.manifest[section][ssrv].get(
            "version", "latest"))

        return True

    @classmethod
    def update_requirements(cls, srv=None, *options):
        """
        Update an image so that it includes depencies requireed by code.

        This function implements the last step to transform the generic environment indicated by
        the dockerimg or dockerfile into the correct environment for the source code.
        """
        if srv is None or srv == "-a":
            for k in list(cls._ocean.manifest.keys()):
                for s in cls._ocean.manifest[k]:
                    cls.update_requirements(s, options)
            return
        return cls._ocean._do_build_built(srv, options)
