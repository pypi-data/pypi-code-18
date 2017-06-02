import itertools
import logging
import os
import shutil
import subprocess
from functools import reduce


class MixIn(object):
    """
    Allows to build or download images as initial step.
    """

    _PIPELINE = [
        (10, "base")
    ]

    @classmethod
    def _pipeline_prev(cls):
        """
        Identify the previous build step in the build pipeline.
        """
        return cls._ocean._PIPELINE[cls._ocean._PIPELINE.index(cls._PIPELINE[-1]) - 1][1]

    @classmethod
    def get_commitid(cls, srv):
        srcp = cls._ocean._get_srcp(srv)
        if os.path.exists(os.path.join(srcp, ".git")):
            p = subprocess.Popen(["git", "describe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=srcp)
            o, e = p.communicate()
            if e:
                p = subprocess.Popen(["git", "log", "-n", "1", "--format=%H"], stdout=subprocess.PIPE, cwd=srcp)
                o, e = p.communicate()
            res = o.decode('utf8')
        else:
            res = "default"
        return res

    @classmethod
    def _buildock(cls, dockerfile, srv, *options):
        """
        Build the container associated with a project.

        :param dockerfile: file to be use by docker build.
        :param srv: name of the project.
        :param options: build options to pass to docker
        :return:
        """
        local = False
        section, ssrv, tag = cls._ocean._find_section_new(srv)

        if "-f" not in options:
            if (cls._ocean.cache_try_pull_image(srv, cls._PIPELINE[0][1] + "-" +
                                                cls._ocean.manifest[section][ssrv].get("version", "latest"))):
                return True

        if section.startswith("local-"):
            local = True

        c_mp = (cls._ocean.MPL if local else cls._ocean.MP)

        if not os.path.exists(os.path.join(c_mp, "dockerfiles", dockerfile)):
            found = False
            for c_mp in itertools.chain([os.path.join(os.path.join(cls._ocean._get_srcp(ssrv, section)), "ocean")],
                                        map(lambda asrv: os.path.join(os.path.join(cls._ocean._get_srcp(asrv, section)),
                                                                      "ocean"), cls._ocean.manifest[section].keys())):
                if os.path.exists(os.path.join(c_mp, "dockerfiles", dockerfile)):
                    found = True
                    break
            if not found:
                logging.error("Can't file DOCKERFILE and build image.")
                raise ValueError(dockerfile)

        if os.path.isdir(os.path.join(c_mp, "dockerfiles", dockerfile)):
            p = cls._ocean._subprocess_popen("docker build  -t %s %s ." % (cls._ocean._image_name(ssrv, "base-latest"),
                                                                           " ".join(options)),
                                             cwd=os.path.join(c_mp, "dockerfiles", dockerfile), shell=True)
            _o, _e = p.communicate()
        else:
            BI = os.path.join(c_mp, "build-internal")
            if os.path.exists(BI):
                shutil.rmtree(BI)

            os.mkdir(BI)
            shutil.copy2(os.path.join(c_mp, "dockerfiles", dockerfile), os.path.join(BI, dockerfile))
            p = cls._ocean._subprocess_popen(
                "docker build -f %s -t %s %s ." % (
                    dockerfile, cls._ocean._image_name(srv, "base-latest"), " ".join(options)),
                cwd=BI, shell=True)
            _o, _e = p.communicate()
            shutil.rmtree(BI)

        ret = (p.returncode == 0)
        if ret:
            cls.cache_push_image(srv, "base-latest", "base-" + cls.get_commitid(srv))
        return ret

    @classmethod
    def cache_try_pull_image(cls, srv, tag):
        """
        Push an image in the local docker repo.
        """
        if tag is None:
            tag = cls._ocean._last_predeploy_tag()

        if cls._ocean._get_config("dock_cache_repo") and not cls._ocean._get_config("disable_cache_update", False):
            cache_image_name = cls._ocean._get_config("dock_cache_repo") + "/" + cls._ocean._image_name(srv) + ":" + tag
            if os.system("docker pull %s" % (cache_image_name)) == 0:
                os.system("docker tag %s %s" % (cache_image_name, cls._ocean._image_name(srv, "base-latest")))
                return True

        return False

    @classmethod
    def cache_push_image(cls, srv, tag=None, ntag=None):
        """
        Push an image in the local docker repo.
        """
        if tag is None:
            tag = cls._ocean._last_predeploy_tag()

        if ntag is None:
            ntag = tag

        if cls._ocean._get_config("dock_cache_repo") and cls._ocean._get_config("enable_cache_upload", False):
            cache_image_name = cls._ocean._get_config("dock_cache_repo") + "/" + cls._ocean._image_name(
                srv) + ":" + ntag
            cmd = "docker tag %s %s" % (cls._ocean._image_name(srv, tag), cache_image_name)
            logging.debug(cmd)
            os.system(cmd)
            cmd = "docker push %s" % (cache_image_name)
            logging.debug(cmd)
            os.system(cmd)

    @classmethod
    def is_built(cls, srv, tag=None, **kwargs):
        """
        Indicate whether a service is built up to specified tag.
        """

        available_docker_images = kwargs.get("di", None)

        imgn = cls._ocean._image_name(srv)

        # by default we try to look for the last build tag.
        if tag is None:
            tag = cls._ocean._last_predeploy_tag()

        if available_docker_images is None:
            available_docker_images = cls._ocean._docker_images(
                img_selector=lambda i: ("%s:%s" % (imgn, tag) in i["RepoTags"]))

        logging.debug("is_built : Looking for image name=%s tag=%s" % (imgn, tag))
        return reduce(lambda b, cd: b or ("%s:%s" % (imgn, tag) in cd["RepoTags"]),
                      available_docker_images.get(imgn, []), False)

    @classmethod
    def _do_build_base(cls, srv=None, *options, **kwargs):
        di = kwargs.get("di", None)
        if di is None:
            di = cls._ocean._docker_images()

        rebuild = False
        if "-f" in options:
            rebuild = True
            indf = options.index("-f")
            options = options[:indf] + options[indf + 1:]

        if cls.is_built(srv, "base-latest"):
            if rebuild:
                o, e = cls._ocean._subprocess_popen("docker rm %s" % (srv,), shell=True).communicate()
            else:
                logging.warning("already built")
                return True

        logging.debug("building :" + srv + "\n")

        section = cls._ocean._find_section(srv)
        srvp = os.path.join(cls._ocean.SRC, section, cls._ocean._src_folder(srv))

        if "pre-build" in cls._ocean.manifest[section][srv]:
            os.system(cls._ocean.manifest[section][srv]["pre-build"])

        if "dockerimg" in cls._ocean.manifest[section][srv]:
            if os.system("docker pull %s" % (cls._ocean.manifest[section][srv]["dockerimg"])) == 0:
                os.system("docker tag %s %s" % (cls._ocean.manifest[section][srv]["dockerimg"],
                                                cls._ocean._image_name(srv, "base-latest"))
                          )
                return True
            return False
        else:
            if "dockerfile" in cls._ocean.manifest[section][srv]:
                dockerfile = cls._ocean.manifest[section][srv]["dockerfile"]
                return cls._buildock(dockerfile, srv)
            else:
                cls._buildock("default.docker", srv)
                if not (os.path.exists(srvp)):
                    return cls._ocean._call_with_eh("clone", srv)

    @classmethod
    def build(cls, srv=None, *options, **kwargs):
        """
        Run all the step necessary to build a container up to a certain level.
        """
        tag = kwargs.get("tag")
        target_level = 100

        if srv is None or srv == "-a":
            di = kwargs.get("di")
            if di is None:
                di = cls._ocean._docker_images()
            for k in list(cls._ocean.manifest.keys()):
                for s in cls._ocean.manifest[k]:
                    try:
                        cls.build(s, *options, di=di)
                    except Exception as e:
                        logging.warning(str(e))
            return

        if "-t" in options:
            tag = options[options.index("-t") + 1]

        if "-tl" in options:
            tag = int(options[options.index("-tl") + 1])

        if "-R" in options:
            logging.info("Looking for %s requirements..." % (srv,))
            for nsrv in cls._ocean._get(srv).get("requires", []):
                logging.info("Checking status of subservice " + nsrv)
                try:
                    cls.build(nsrv, *options)
                except BaseException:
                    logging.warning("Could not build " + nsrv)

        if cls._ocean._get(srv).get("type", "service") in ["environment"]:
            return True

        if cls._ocean._get(srv).get("no-container"):
            return True

        force = "-f" in options
        logging.debug("Build target for '%s' to stage '%s'" % (srv, tag))

        for btag in filter(lambda x: x[0] <= target_level, cls._ocean._PIPELINE):
            if tag and btag[1] == tag:
                break
            tag = btag[1] + "-latest"
            if force or not cls.is_built(srv, tag):
                r = cls._ocean._call_with_eh("_do_build_" + btag[1], srv, *options, **kwargs)
                if not r:
                    logging.warning("build %s step %s failed" % (srv, btag))
                    return r

        return True
