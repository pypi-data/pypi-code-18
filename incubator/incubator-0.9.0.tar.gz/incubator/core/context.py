"""
Classes for manipulating with build and global context.
"""
import os
import tarfile

import six

from .fileutils import (get_filtered_files, is_top_file, normalise_patterns,
                        remove_top_parent)


class BuildContext:
    """
    Contains the build context files and provides the access to them.
    """

    def __init__(self, context, limit):
        self._context = context
        self._struct = None
        self._context.seek(0)
        self.limit = limit

    @property
    def structure(self):
        """
        List of files in the context.
        """
        if not self._struct:
            self._context.seek(0)
            with tarfile.open(mode="r", fileobj=self._context) as tar_file:
                self._struct = tar_file.getnames()
            self._context.seek(0)
        return self._struct

    def get_file(self, name):
        """
        Get a file from context by its name.

        * name: path of the file in the context
        * **return:** file-object, if the file is present in the context
        """
        try:
            with tarfile.open(mode="r", fileobj=self._context) as tar:
                f = tar.extractfile(tar.getmember(name))
            if not f:
                return None
            file = six.BytesIO()
            file.writelines(f.readlines())
            file.seek(0)
            return file
        except:
            return None
        finally:
            self._context.seek(0)

    def get_archive(self, patterns, single_file=None):
        """
        Create archive from the context with given patterns.

        * patterns: list of shell wildcard patterns
        * single_file: if specified, the source has to be one file
        * **return:** archive as a file-like object
        """

        normpatterns = normalise_patterns(patterns)

        with tarfile.open(mode="r", fileobj=self._context) as tar_file:

            put_all = os.curdir in normpatterns

            files_to_put = self.structure if put_all else get_filtered_files(self.structure, normpatterns, tar_file)

            if len(files_to_put) == 0:
                return None
            elif single_file and len(files_to_put) > 1:
                raise ValueError("expecting single file in patterns: {}".format(normpatterns))

            tar_in_memory = six.BytesIO()
            with tarfile.open(mode="w", fileobj=tar_in_memory) as filtered_tar:
                for file in files_to_put:
                    file_info = tar_file.getmember(file)
                    file_object = tar_file.extractfile(file_info)
                    if single_file:
                        file_info.name = single_file
                    elif not put_all and is_top_file(file):
                        file_info.name = remove_top_parent(file)
                    filtered_tar.addfile(tarinfo=file_info,
                                         fileobj=file_object)

            tar_in_memory.seek(0)
            self._context.seek(0)
            return tar_in_memory


class GlobalContext(object):
    """
    Global context for the build process.
    Contains envs, workdir and user.
    """

    def __init__(self, envs=None, workdir=None, user=None, buildargs=None):
        self.envs = envs or {}
        self.workdir = workdir or os.path.curdir
        self._unused_buildargs = set(buildargs)
        self.user = user

    @property
    def unused_buildargs(self):
        """
        Build arguments, that were not used during the build.
        """
        return self._unused_buildargs

    def use_buildarg(self, key, value):
        """
        Mark buildarg as used and update the dictionary with environment variables.
        * key: name of the build argument
        * value: value of the build argument
        """
        if key in self.unused_buildargs:
            self.unused_buildargs.remove(key)
        self.envs[key] = value
