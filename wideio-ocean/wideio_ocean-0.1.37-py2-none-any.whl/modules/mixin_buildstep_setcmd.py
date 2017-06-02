import json
import logging
import os
import pipes
import shlex
import shutil
import sys
import uuid


def safe_escape(s):
    if sys.version_info < (3, 3):
        return pipes.quote(s)
    else:
        return shlex.quote(s)


class MixIn(object):
    """
    Reset the default command line associated with an image and set labels.

    (even after commit with the source dir)
    """

    _PIPELINE = [
        (95, "ready")
    ]

    @classmethod
    def _pipeline_prev(cls):
        """
        Identify the previous build step in the build pipeline.
        """
        return cls._ocean._PIPELINE[cls._ocean._PIPELINE.index(cls._PIPELINE[-1]) - 1][1]

    @classmethod
    def _normalize_items(cls, item):
        """Recursively transform sets into lists"""
        if type(item) in [list, set, tuple]:
            return list(map(cls._normalize_items, item))
        elif isinstance(item, dict):
            return dict(map(lambda i: (i[0], cls._normalize_items(i[1])), item.items()))
        else:
            return item

    @classmethod
    def _do_build_ready(cls, srv=None, *options, **kwargs):
        """
        Update the command associated with a container.
        """
        if "-f" not in options:
            if cls._ocean.cache_try_pull_image(srv, cls._PIPELINE[0][1] + "-latest"):
                return True

        section, srv, tag = cls._ocean._find_section_new(srv)

        prev = cls._ocean._image_name(srv, cls._pipeline_prev() + "-latest")

        logging.debug("Setting command and labels for container")
        tmpid = "/tmp/" + str(uuid.uuid4())
        os.makedirs(tmpid)
        labels = "LABEL " + " " .join(["OCEAN.%s=%s" % (
            i[0].upper().replace('-', '_'),
            safe_escape(json.dumps({'@value': cls._normalize_items(i[1])}))
        )
            for i in cls._ocean.manifest[section][srv].items()
        ])
        labels += (" VERSION=%s" % (cls._ocean.get_commitid(srv)))
        tcmd = cls._ocean.manifest[section][srv].get("command")
        if tcmd is None:
            tcmd = ""
        else:
            tcmd = "CMD " + tcmd
        with open(os.path.join(tmpid, "Dockerfile"), "w") as f:
            f.write(
                (
                    """
FROM %s
%s
%s
            """ % (prev,
                        labels,
                        tcmd)
                ).strip()
            )

        logging.debug("build:" + cls._ocean.manifest[section][srv].get("version", "latest"))

        cmd = "docker build  -t %s ." % (
            cls._ocean._image_name(srv, cls._PIPELINE[0][1] + "-" + cls._ocean.manifest[section][srv].get(
                "version", "latest"))
        )
        logging.debug(cmd)
        _o, _e = cls._ocean._subprocess_popen(cmd, shell=True, cwd=tmpid).communicate()

        # cleanup
        shutil.rmtree(tmpid)

        cls._ocean.cache_push_image(srv, "ready-" + cls._ocean.manifest[section][srv].get(
            "version", "latest"), "ready-" + cls._ocean.get_commitid(srv))

        return True
