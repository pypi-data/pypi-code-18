"""
Classes for manipulating with the container engine.
"""

import ast
import logging
import re
from distutils.version import StrictVersion
from time import sleep

import docker
from docker.errors import APIError
from docker.utils import exclude_paths

from .constants import (APP_NAME, DEFAULT_INFINITE_COMMAND, MAX_API_ATTEMPTS,
                        TIME_TO_NEXT_ATTEMPT)
from .history import ContainerHistory
from .output import CHAPTER, ERROR_SUBTITLE
from .parsing import get_name_and_tag, quote
from .utilclasses import Volume

_IS_OLD_API = StrictVersion(docker.__version__) < StrictVersion('2.0.0')

_logger = logging.getLogger(APP_NAME)


class Client:
    """
    Abstract container client representing basic functionality of container engine.
    """

    def __init__(self, history=None):
        self.history = history or ContainerHistory()

    def build_image(self, fileobj=None, dockerfile=None, custom_context=None, buildargs=None, path=None):
        """
        Build image from given dockerfile, context and build arguments.

        * fileobj: file-like object representing dockerfile or archive with context
        * dockerfile: path to dockerfile in build context
        * custom_context: whether to use fileobj as context
        * buildargs: build arguments passed to build
        * path: directory with build context
        * **return:** id of created image
        """
        pass

    def run_container_infinitely(self, image, infinite_command=None, volumes=None, container_limits=None):
        """
        Run a container with infinite command.
        Container is created, never stop and can be changed via exec.

        * image: image used for new container
        * infinite_command: infinite_command can be overwritten (default is in constants.py)
        * volumes: volumes mounted to container
        * container_limits: (dict) A dictionary of limits applied to each container created by the build process. Valid keys:
                    memory (int): set memory limit for build
                    memswap (int): Total memory (memory + swap), -1 to disable swap
                    cpushares (int): CPU shares (relative weight)
                    cpusetcpus (str): CPUs in which to allow execution, e.g., "0-3", "0,1"
        * **return:** id of created container
        """
        pass

    def run_container(self, image, command):
        """
        Run a container with givent command.

        * image: container image to run
        * command: command to run in container
        * **return:** output from command
        """
        pass

    def commit_container(self, container, conf, author, message, tags=None):
        """
        Create new image from container.

        * container: id of container to commit
        * conf: configuration forced to client
        * author: author of commit
        * message: commit message
        * tags: (list of tuples) tags connected to new image
        * **return:** id of created image
        """
        pass

    def execute(self, container, cmd, envs, user):
        """
        Create new image from container.

        * container: id of container to commit
        * conf: configuration forced to client
        * author: author of commit
        * message: commit message
        * tags: (list of tuples) tags connected to new image
        * **return:** id of created image
        """
        pass

    def put_archive(self, container, path, data):
        """
        Put archive into container.

        * container: id of container to put data in
        * path: where to put data
        * data: archive with data
        * **return:** None
        """
        pass

    def remove_container(self, container):
        """
        Remove container.

        * container: id of container to remove
        * **return:** None
        """
        pass

    def remove_image(self, image):
        """
        Remove image.

        * image: Id of image to remove.
        * **return:** None
        """
        pass

    def get_image(self, name):
        """
        Get id of image with given name.

        * name: name or id of image
        * **return:** id of image with given name or None
        """
        pass

    def pull_image(self, name):
        """
        Pull image with given name from repository.

        * name: Name of image to pull. Default tag is 'latest'.
        * **return:** Id of pulled image or None.
        """
        pass

    def get_image_info(self, image):
        """
        Return information about the image (like `docker inspect image_id`

        * image: id or name of the image
        * **return:** dict with information about the given image
        """

    @staticmethod
    def exclude_paths_from_context(root, exclude, dockerfile):
        """
        * root: path of build context
        * exclude: list of `.dockerignore` patterns
        * dockerfile: path to dockerfile
        * **return:** iterator of all paths (files and directories) not excluded with patterns
                    All paths returned are relative to the root.
        """
        pass


class DockerClient(Client):
    """
    Container client representing docker-py independently to version of *Docker-py*.
    """

    def __init__(self, history=None):
        Client.__init__(self, history)
        self.client = docker.from_env(version='auto')

    def build_image(self, fileobj=None, dockerfile=None, custom_context=None, buildargs=None, path=None):
        if _IS_OLD_API:
            resp = [line for line in self.client.build(rm=True, fileobj=fileobj,
                                                       dockerfile=dockerfile,
                                                       custom_context=custom_context,
                                                       buildargs=buildargs,
                                                       path=path
                                                       )]
            event = ast.literal_eval(resp[-1].decode())
            if 'stream' in event:
                match = re.search(r'Successfully built ([0-9a-f]+)',
                                  event.get('stream', ''))
                if match:
                    image_id = match.group(1)
                    return image_id
        else:
            image = self.client.images.build(rm=True, fileobj=fileobj,
                                             dockerfile=dockerfile,
                                             custom_context=custom_context,
                                             buildargs=buildargs,
                                             path=path)
            return image.id

    def run_container_infinitely(self, image, infinite_command=None, volumes=None, container_limits=None):
        infinite_command = infinite_command or DEFAULT_INFINITE_COMMAND
        volumes = volumes or {}
        container_limits = container_limits or {}

        if _IS_OLD_API:
            client = self.client
        else:
            client = self.client.api

        volumes_list = Volume.volumes_to_list(volumes)
        container_id = client.create_container(image=image,
                                               command=infinite_command,
                                               host_config={"binds": volumes_list,
                                                            "Memory": container_limits.get("memory"),
                                                            'MemorySwap': container_limits.get("memswap"),
                                                            'CpuShares': container_limits.get("cpushares"),
                                                            'CpusetCpus': container_limits.get("cpusetcpus")
                                                            },
                                               stdin_open=True).get('Id')
        self.history.add_container_status(id=container_id,
                                          state="created")
        client.start(container_id)
        self.history.add_container_status(id=container_id,
                                          state="running")
        return container_id

    def run_container(self, image, command, remove=False, volumes=None, container_limits=None):
        volumes = volumes or {}
        container_limits = container_limits or {}
        if _IS_OLD_API:
            volumes_list = Volume.volumes_to_list(volumes)
            container_id = self.client.create_container(image=image,
                                                        command=command,
                                                        host_config={"binds": volumes_list,
                                                                     "Memory": container_limits.get("memory"),
                                                                     'MemorySwap': container_limits.get("memswap"),
                                                                     'CpuShares': container_limits.get("cpushares"),
                                                                     'CpusetCpus': container_limits.get("cpusetcpus")
                                                                     },
                                                        ).get('Id')
            self.history.add_container_status(id=container_id,
                                              state="created")
            self.client.start(container_id)
            self.history.add_container_status(id=container_id,
                                              state="running")

            # TODO: temporary workaround !!!
            self.client.wait(container_id)

            for l in self.client.logs(container=container_id,
                                      stream=True, follow=True,
                                      stdout=True, stderr=True,
                                      tail='all'):
                yield l

            self.history.add_container_status(id=container_id,
                                              state="stopped")
            if remove:
                self.client.remove_container(container_id, force=True)
                self.history.remove_container(id=container_id)

        else:
            volumes_list = Volume.volumes_to_bind_dict(volumes)
            container = self.client.containers.create(image=image,
                                                      command=command,
                                                      volumes=volumes_list,
                                                      mem_limit=container_limits.get("memory"),
                                                      memswap_limit=container_limits.get("memswap"),
                                                      cpu_shares=container_limits.get("cpushares"),
                                                      cpuset_cpus=container_limits.get("cpusetcpus"))
            self.history.add_container_status(id=container.id,
                                              state=container.status)

            container.start()

            self.history.add_container_status(id=container.id,
                                              state=container.status)

            # TODO: temporary workaround !!!
            container.wait()

            for l in container.logs(stream=True, follow=True, stdout=True, stderr=True, tail='all'):
                yield l

            self.history.add_container_status(id=container.id,
                                              state="stopped")

            if remove:
                container.remove(force=True)
                self.history.remove_container(container.id)

    def commit_container(self, container, conf, author, message, tags=None):
        tags = tags or []
        if _IS_OLD_API:
            image_id = self.client.commit(container=container,
                                          conf=conf,
                                          author=author,
                                          message=message).get('Id')
            self.history.add_container_status(container, "committed", "- image: {}".format(image_id))

            for repo, tag in tags:
                self.client.tag(image=image_id,
                                repository=repo,
                                tag=tag)
                _logger.debug(
                    CHAPTER.format("image tagged:\n- id: {}\n- repo: {}\n- tag: {}".format(image_id, repo, tag)))
            return image_id
        else:
            container_obj = self.client.containers.get(container)
            image = container_obj.commit(conf=conf,
                                         author=author,
                                         message=message)
            self.history.add_container_status(container, "committed", "- image: {}".format(image.id))
            for repo, tag in tags:
                image.tag(repo, tag)
                _logger.debug(
                    CHAPTER.format("image tagged:\n- id: {}\n- repo: {}\n- tag: {}".format(image.id, repo, tag)))
            return image.id

    def execute(self, container, cmd, envs=None, user=None):
        envs = envs or {}

        if _IS_OLD_API:
            env_string = " ".join(["{}={}".format(k, quote(v)) for k, v in envs.items()])
            cmd = "{} {}".format(env_string, cmd)

        cmd = "sh -c {}".format(quote(cmd))

        if _IS_OLD_API:
            command_id = self.client.exec_create(container=container,
                                                 cmd=cmd,
                                                 user=user).get('Id')
            output = self.client.exec_start(exec_id=command_id,
                                            stream=True)
        else:
            container_obj = self.client.containers.get(container)
            output = container_obj.exec_run(cmd=cmd,
                                            stream=True,
                                            environment=envs,
                                            user=user)
        return output

    def put_archive(self, container, path, data):
        for i in range(MAX_API_ATTEMPTS):
            try:
                if _IS_OLD_API:
                    self.client.put_archive(container=container,
                                            path=path,
                                            data=data)
                else:
                    container_obj = self.client.containers.get(container)
                    container_obj.put_archive(path=path, data=data)
            except Exception as exc:
                _logger.warning(ERROR_SUBTITLE.format("fail to send data to the container (repeating)"))
                if i == MAX_API_ATTEMPTS:
                    raise exc
                sleep(TIME_TO_NEXT_ATTEMPT)

    def stop_container(self, container):
        if _IS_OLD_API:
            self.client.kill(container)
            self.history.add_container_status(container, "stopped")
        else:
            container_obj = self.client.containers.get(container)
            container_obj.kill()
            self.history.add_container_status(container, "stopped")

    def remove_container(self, container):
        if _IS_OLD_API:
            self.client.remove_container(container)
            self.history.remove_container(container)
        else:
            container_obj = self.client.containers.get(container)
            container_obj.remove()
            self.history.remove_container(container)

    def remove_image(self, image):
        if _IS_OLD_API:
            self.client.remove_image(image)
        else:
            image_obj = self.client.images.get(image)
            image_obj.remove()

    def get_image(self, name):
        try:
            if _IS_OLD_API:
                image = self.client.inspect_image(name)
                if image:
                    return image.get('Id')
            else:
                image = self.client.images.get(name)
                if image:
                    return image.id
        except APIError:
            return None
        return None

    def pull_image(self, name):
        image_name, image_tag = get_name_and_tag(name)

        if _IS_OLD_API:
            self.client.pull(repository=image_name,
                             tag=image_tag)
            return self.get_image(name)
        else:
            image = self.client.images.pull("{}:{}".format(image_name, image_tag))
            if image:
                return image.id
        return None

    def get_image_info(self, image):
        try:
            if _IS_OLD_API:
                return self.client.inspect_image(image)
            else:
                image = self.client.images.get(image)
                return image.attrs
        except Exception:
            return None

    @staticmethod
    def exclude_paths_from_context(root, exclude, dockerfile):
        return exclude_paths(root, exclude, dockerfile)
