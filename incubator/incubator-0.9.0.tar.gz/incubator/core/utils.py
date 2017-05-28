"""
Utility methods for builder.
"""
import io
import logging
import os
import tarfile
import tempfile

import six

from .constants import (APP_NAME, CONTEXT_FILE_IN_MEMORY, CONTEXT_FILE_ON_DISK,
                        DEFAULT_CONTEXT_FILE_LIMIT)
from .fileutils import change_tarinfo_properties
from .output import CHAPTER

_logger = logging.getLogger(APP_NAME)


def dockerfile_from_context(context, path):
    """
    Get a *Dockerfile* file-like object from the archive with the build context.

    * context: tar archive with the build context
    * path: *Dockerfile* location in the build context
    * **return:** file-like *Dockerfile* content
    """
    with tarfile.open(mode="r", fileobj=context) as t:
        df = t.extractfile(t.getmember(path))
    dockerfile = six.BytesIO()
    dockerfile.writelines(df.readlines())
    dockerfile.seek(0)
    context.seek(0)
    return dockerfile


def mkbuildcontext(path, fileobj, custom_context, dockerfile, client, limit=None):
    """
    Make a build context from the variety of arguments.

    * path: file-path to the build context
    * fileobj: file-like object representing *Dockerfile* or build context with *Dockerfile*
    * custom_context: whether to use custom context
    * dockerfile: *Dockerfile* location in the build context
    * client: containerization client
    * limit: limit of context size to save context in memory
    * **return:** tuple:
        - context file-like object
        - *Dockerfile* file-like object
    """
    if path is None and fileobj is None:
        raise TypeError("Either path or fileobj needs to be provided.")

    dockerfile = dockerfile or "Dockerfile"

    if custom_context:
        if not fileobj:
            raise TypeError("You must specify fileobj with custom_context")
        return fileobj, dockerfile_from_context(fileobj, dockerfile)
    elif fileobj is not None:
        return make_build_context_from_dockerfile(fileobj), fileobj
    elif path.startswith(('http://', 'https://',
                          'git://', 'github.com/', 'git@')):
        # TODO
        return None, None
    elif not os.path.isdir(path):
        raise TypeError("You must specify a directory to build in path")
    else:
        dockerignore = os.path.join(path, '.dockerignore')
        exclude = None
        if os.path.exists(dockerignore):
            with open(dockerignore, 'r') as f:
                exclude = list(filter(bool, f.read().splitlines()))
        context = tar(
            path, client, exclude=exclude, dockerfile=dockerfile, limit=limit
        )
        dockerfile_obj = dockerfile_from_context(context=context, path=dockerfile)
        return context, dockerfile_obj


def exclude_paths(root, exclude, dockerfile, client):
    """
    Exclude paths from the build context.

    * root: root file path
    * exclude: exclude patterns
    * dockerfile: *Dockerfile* file-path in the context
    * client: containerization context
    * **return:** filtered files
    """
    files = client.exclude_paths_from_context(root, exclude, dockerfile)
    return files


def tar(path, client, exclude=None, dockerfile=None, fileobj=None, limit=DEFAULT_CONTEXT_FILE_LIMIT):
    """
    Make an archive with the build context.

    * path: to build context
    * client: containerization client
    * exclude: exclude patterns
    * dockerfile: of the *Dockerfile* in the build context
    * fileobj: file-object representation of the *Dockerfile* or build context with the *Dockerfile*
    * limit: limit of context size to save context in memory
    * **return:** fil-like object with the build context
    """
    if not fileobj:
        fileobj = tempfile.SpooledTemporaryFile(max_size=limit)

    root = os.path.abspath(path)
    exclude = exclude or []

    _logger.debug(CHAPTER.format("context:"))
    with tarfile.open(mode='w', fileobj=fileobj) as t:
        for p in sorted(exclude_paths(root, exclude,
                                      dockerfile=dockerfile,
                                      client=client)):
            _logger.debug("- {}".format(p))
            t.add(name=os.path.join(path, p), arcname=p, filter=change_tarinfo_properties)
    _logger.debug("")
    fileobj.seek(0)

    if isinstance(fileobj, tempfile.SpooledTemporaryFile):
        if fileobj.name:
            context_file_type = CONTEXT_FILE_ON_DISK
        else:
            context_file_type = CONTEXT_FILE_IN_MEMORY
        _logger.debug(CHAPTER.format("context type: {}".format(context_file_type)))

    return fileobj


def make_build_context_from_dockerfile(dockerfile):
    """
    Make a build context file object from the provided *Dockerfile*.

    * dockerfile: file-like object with the *Dockerfile* content
    * **return:** file-like object with the build context
    """
    f = six.BytesIO()
    with tarfile.open(mode='w', fileobj=f) as t:
        if isinstance(dockerfile, six.StringIO) or isinstance(dockerfile, io.StringIO):
            dfinfo = tarfile.TarInfo('Dockerfile')
            dfinfo.size = len(dockerfile.getvalue())
            dockerfile.seek(0)
        elif isinstance(dockerfile, six.BytesIO) or isinstance(dockerfile, io.BytesIO):
            dfinfo = tarfile.TarInfo('Dockerfile')
            dfinfo.size = len(dockerfile.getvalue())
            dockerfile.seek(0)
        else:
            dfinfo = t.gettarinfo(fileobj=dockerfile, arcname='Dockerfile')
        t.addfile(dfinfo, dockerfile)
    f.seek(0)
    return f


def get_list_from_tuple_or_string(value):
    """
    Make a list of strings from given value.

    * value: None, string or list of strings
    * **return:** list with strings
    """
    if not value:
        return []
    if isinstance(value, six.string_types):
        return [value]
    else:
        return list(value)
