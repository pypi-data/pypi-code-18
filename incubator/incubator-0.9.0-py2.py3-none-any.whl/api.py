"""
Python API for building docker images in better and more secure way.
"""

import logging

from .core import utils
from .core.build import Builder
from .core.caching import ImageCache
from .core.client import DockerClient
from .core.config import ImageConfig
from .core.constants import APP_NAME
from .core.context import BuildContext
from .core.output import ERROR_SUBTITLE
from .core.utilclasses import Volume

_logger = logging.getLogger(APP_NAME)


def build(path=None, fileobj=None, tag=None,
          custom_context=False, pull=False, rm=False,
          forcerm=False, dockerfile=None, buildargs=None,
          container_limits=None, volumes=None, layers=None,
          labels=None, config=None, context_file_limit=None,
          container_client=None, cache=None):
    """
    Build a container image from provided build context and Dockerfile.

    * path: (str) path to the directory containing *Dockerfile*
    * fileobj: a file object to use as *Dockerfile* (or a file-like
                object, e.g. `BytesIO`)
    * tag: (str) tag to add to the final image
    * custom_context: (bool) optional if using `fileobj`
    * pull: (bool) downloads any updates to the `FROM` image in *Dockerfile*
    * rm: (bool) remove intermediate containers
                The `docker build` command now defaults to `--rm=true`,
                but we have kept the old
                default of `False` to preserve backward compatibility.
    * forcerm: (bool) always remove intermediate containers,
                even after unsuccessful build
    * dockerfile: (str) path within the build context to the *Dockerfile*
    * buildargs:  (dict) dictionary of build arguments
    * container_limits: (dict) A dictionary of limits applied to each
                    container created by the build process.
                    Valid keys:
        - memory (int): set memory limit for build
        - memswap (int): total memory (memory + swap), -1 to disable swap
        - cpushares (int): CPU shares (relative weight)
        - cpusetcpus (str): CPUs in which to allow execution, e.g., `0-3`, `0,1`
    * labels: (dict) dictionary of labels to set on the image
    * volumes: (list) list of bind volumes (str or `Volume` instance)
    * layers: (list) list of layer splits
    * config: (dict or list of dicts) dictionary of addition configuration
    * context_file_limit: (int) maximum size of in memory config (0 is unlimited and default)
    * cache: object responsible for caching images
    * container_client: client representing basic container API

    * **return:** `ResultImage` instance
    """

    try:
        container_client = container_client or DockerClient()
    except Exception as ex:
        _logger.warning(ERROR_SUBTITLE.format("Cannot launch container client:\n{}".format(ex)))
        raise ex

    cache = cache or ImageCache()

    try:
        config_object = ImageConfig.merge_configs(config)
    except Exception as ex:
        _logger.warning(ERROR_SUBTITLE.format("Cannot merge config files:\n{}".format(ex)))
        raise ex

    try:
        config_object.update(buildargs=buildargs,
                             container_limits=container_limits,
                             context_file_limit=context_file_limit,
                             forcerm=forcerm,
                             labels=labels,
                             layers=layers,
                             pull=pull,
                             rm=rm,
                             tags=tag,
                             volumes=Volume.get_instances(volumes))
    except Exception as ex:
        _logger.warning(ERROR_SUBTITLE.format("Cannot update config with arguments:\n{}".format(ex)))
        raise ex

    try:
        context_fileobj, dockerfile_fileobj = utils.mkbuildcontext(path=path,
                                                                   fileobj=fileobj,
                                                                   custom_context=custom_context,
                                                                   dockerfile=dockerfile,
                                                                   client=container_client,
                                                                   limit=config_object.context_file_limit)
        build_context = BuildContext(context=context_fileobj, limit=context_file_limit)

    except Exception as ex:
        _logger.warning(ERROR_SUBTITLE.format("Cannot make build context:\n{}".format(ex)))
        raise ex

    try:
        builder = Builder(context=build_context,
                          dockerfile=dockerfile_fileobj,
                          client=container_client,
                          config=config_object,
                          cache=cache)
        return builder.build()
    except Exception as ex:
        _logger.warning(ERROR_SUBTITLE.format("Build failed:\n{}".format(ex)))
        raise ex
