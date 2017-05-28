"""
Core functionality for building container images.
"""

import logging

from .commands import get_layers_from_dockerfile_structure
from .constants import APP_NAME
from .context import GlobalContext
from .output import CHAPTER, ERROR_SUBTITLE, SUBTITLE, TITLE
from .parsing import create_dockerfile_structure
from .utilclasses import ResultImage

_logger = logging.getLogger(APP_NAME)


class Builder:
    """
    Class allowing the image build process.
    """

    def __init__(self, context, dockerfile, client, config, cache):
        """
        * context: build context that will be loaded during the build
                    and that can be used as a source for `ADD` and `COPY`.
        * dockerfile: file-like object with the *Dockerfile* content
        * client: container client
                    (allowing the basic operation with images and containers)
        * config: instance of *Config* class
        * cache: object with cache ability
        """

        self.client = client

        self._context = context
        self._config = config
        self._cache = cache
        self._dockerfile = dockerfile
        self._cmd_structure, self._env_label_structure, self._base_image = create_dockerfile_structure(
            dockerfile_content=self._dockerfile)

    def build(self):
        """
        Build an image from given *Dockerfile*, context and configuration.
        Using given container client.

        * **return:** id of final image
        """

        logs = []
        last_image = None
        current_layer = None
        global_context = GlobalContext(buildargs=self._config.buildargs)
        layers = get_layers_from_dockerfile_structure(structure=self._cmd_structure,
                                                      env_label_context=self._env_label_structure,
                                                      layers=self._config.layers,
                                                      global_context=global_context)

        self._prebuild()

        try:
            for current_layer in layers:
                _logger.info(TITLE.format(" LAYER {} ".format(current_layer.number)))
                cached_image = self._cache.get_layer(last_image, current_layer)
                if cached_image:
                    last_image = cached_image
                else:
                    self._create_new_layer(layer=current_layer,
                                           image=last_image)
                    for cmd in current_layer.commands:
                        cmd(client=self.client,
                            layer_context=current_layer.context,
                            build_context=self._context,
                            config=self._config)

                    if not current_layer.is_last:
                        last_image, _logs = self._middle_commit(layer=current_layer,
                                                                last_image=last_image)
                        logs += _logs

            last_image, _logs = self._final_commit(layer=layers[-1],
                                                   last_image=last_image)
            logs += _logs

        except Exception as ex:
            if self._config.forcerm:
                last_container = current_layer.context.current_container
                if last_container in self.client.history.containers:
                    self.client.remove_container(container=last_container)
            raise ex

        self._postbuild()

        if len(global_context.unused_buildargs) > 0:
            b_args = "\n- ".join(self._config.unused_buildargs)
            _logger.warning(ERROR_SUBTITLE.format("Not used build arguments:\n- {}".format(b_args)))

        return ResultImage(image_id=last_image, logs=logs)

    def _create_base_container(self):
        """
        Create a base container filled in *Dockerfile*.

        * **return:** id of a base container
        """
        _logger.debug(CHAPTER.format("base image: {}".format(self._base_image)))

        if self._config.pull or self.client.get_image(self._base_image) is None:
            self.client.pull_image(self._base_image)

        return self.client.run_container_infinitely(
            image=self._base_image,
            infinite_command=self._config.infinite_command,
            volumes=self._config.volumes,
            container_limits=self._config.container_limits)

    def _create_new_layer(self, layer, image):
        """
        Run a new container for the current layer.

        * layer: current `ImageLayer` instance
        * image: image to use for the container
                If not present, the base image from *Dockerfile* is used.
        * **return:** id of newly created container for the current layer
        """
        if not image:
            layer.context.current_container = self._create_base_container()
        else:
            layer.context.current_container = self.client.run_container_infinitely(
                image=image,
                infinite_command=self._config.infinite_command,
                volumes=self._config.volumes,
                container_limits=self._config.container_limits)

    def _final_commit(self, layer, last_image):
        """
        Run a final commit of the image and tag it with the tags from the configuration.

        * layer: current `ImageLayer` instance
        * last_image: id of the last image
        * **return:** tuple (id of the committed image and logs)
        """
        self.client.stop_container(layer.context.current_container)
        _logger.debug(TITLE.format(" FINAL COMMIT "))
        layer.context.update_labels(self._config.labels)
        image = self.client.commit_container(layer.context.current_container,
                                             conf=layer.context.commit_config,
                                             author=layer.context.author,
                                             message=layer.commit_message,
                                             tags=self._config.tags_and_repos)
        self._cache.add(image_id=image,
                        parent_id=last_image,
                        layer=layer)

        last_image = image
        if self._config.rm:
            self.client.remove_container(layer.context.current_container)

        return last_image, layer.context.logs

    def _middle_commit(self, layer, last_image):
        """
        Provide the commit between the two layers.

        * layer: current `ImageLayer` instance
        * last_image: id of the last used image
        * **return:** tuple (id of the committed image and logs)
        """
        self.client.stop_container(layer.context.current_container)
        _logger.debug(TITLE.format(" COMMIT "))
        image = self.client.commit_container(layer.context.current_container,
                                             conf=layer.context.commit_config,
                                             author=layer.context.author,
                                             message=layer.commit_message)

        self._cache.add(image_id=image,
                        parent_id=last_image,
                        layer=layer)

        last_image = image

        if self._config.rm:
            self.client.remove_container(layer.context.current_container)
        return last_image, layer.context.logs

    def _prebuild(self):
        """
        For the future use.
        """
        _logger.debug(SUBTITLE.format('prebuild'))

    def _postbuild(self):
        """
        For the future use.
        """
        _logger.debug(SUBTITLE.format('postbuild'))
