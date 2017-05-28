"""
Utility methods used for files and archives manipulation and filtering.
"""
import fnmatch
import logging
import os

from .constants import APP_NAME, FILE_MODE_FROM_URL

_logger = logging.getLogger(APP_NAME)


def match_filters(file, patterns):
    """
    * file: path of the file
    * patterns: list of shell wildcard patterns
    * **return:** True, if at least one pattern satisfy the given file path
    """
    for p in patterns:
        if fnmatch.fnmatchcase(file, p):
            return True
    return False


def filter_files(files, patterns):
    """
    Filter files with given patterns.

    * files: list of file-paths
    * patterns: list of shell wildcard patterns
    * **return:** list of files, that satisfy at least one pattern
    """
    filtered_files = []

    for f in files:
        if match_filters(f, patterns):
            filtered_files.append(f)
    return filtered_files


def get_filtered_files(files, patterns, tar):
    """
    Get file-object from the archive that satisfies the given patterns.

    * files: list of file-paths
    * patterns: list of shell wildcard patterns
    * tar: tar archive
    * **return:** List of file-like objects, that satisfies the patterns
    """
    root_dirs = []

    filtered_objects = set([])
    for f in files:
        if match_filters(f, patterns):
            fi = tar.getmember(f)
            if fi.isfile():
                filtered_objects.add(f)
            elif fi.isdir():
                root_dirs.append(f)

    root_dirs.sort(key=len)
    for d in root_dirs:
        pattern = "{}{}*".format(d.split(os.sep)[-1],
                                 os.sep)
        matched_subfiles = filter_files(files, [pattern])
        if len(matched_subfiles) == 0:
            if len(d.split(os.sep)) > 1:  # empty subdirectory
                filtered_objects.add(d)
        else:
            filtered_objects.update(matched_subfiles)
            for subfile in matched_subfiles:
                if subfile in root_dirs:
                    root_dirs.remove(subfile)
    return filtered_objects


def change_tarinfo_properties(tarinfo):
    """
    Filter for insertion local file to tar archive.

    * tarinfo: tarinfo to insert
    * **return:** original tarinfo with changed permissions
    """
    tarinfo.uid = 0
    tarinfo.gid = 0
    return tarinfo


def change_tarinfo_properties_mode(tarinfo):
    """
    Filter for insertion not-local file to tar archive.

    * tarinfo: tarinfo to insert
    * **return:** original tarinfo with changed permissions
    """
    tarinfo.uid = 0
    tarinfo.gid = 0
    tarinfo.mode = FILE_MODE_FROM_URL
    return tarinfo


def normalise_patterns(patterns):
    """
    Normalize the path in the pattern.
    * patterns: list of patterns
    * **return:** list of normalized patterns
    """
    return [os.path.normpath(p) for p in patterns]


def remove_top_parent(path):
    """
    Remove the most top parent in the file path.
    """
    return os.sep.join(path.split(os.sep)[1:])


def is_top_file(path):
    """
    Test, if the path is in the top directory.
    """
    return len(path.split(os.sep)) > 1


def put_archive(client, config, container, tar, target):
    """
    Send an archive with data to the container.

    * client: containerization client to use
    * config: build configuration
    * container: id of the current container
    * tar: archive with files to send
    * target: destination path to send data in
    """
    _logger.debug('------> creating target folder:\n{}\n'.format(target))
    create_directory(client, config, container, target)
    _logger.debug('------> sending data to the container')
    client.put_archive(container=container,
                       path=target,
                       data=tar.getvalue())


def create_directory(client, config, container, target):
    """
    Create recursively directory in the container.

    * client: containerization client
    * config: build configuration
    * container: id of the current container
    * target: directory to create
    """
    client.execute(container=container,
                   cmd=config.mkdir_command + ' {}'.format(
                       target))


def copy_files_to_container(container, client, config, context, source, target):
    """
    Copy files to the container.

    * container: id of the current container
    * client: containerization client
    * config: build configuration
    * context: build context with the source files
    * source: list of source patterns
    * target: destination path
    """
    single_file = None
    if target != os.curdir and target[-1] != os.path.sep:  # destination is file
        single_file = os.path.basename(target)
        target = os.path.dirname(os.path.join(os.curdir, target))

    tar = context.get_archive(patterns=source,
                              single_file=single_file)

    if not tar:
        _logger.warning('------> nothing to copy\n{}'.format(target))
        return

    put_archive(client, config, container, tar, target)


def norm_path_with_work_dir(path, workdir):
    """
    Normalize the path relatively to the current working directory.

    * path: file path to normalize
    * workdir: current working directory
    * **return:** file-path, that was make relative to working directory and normalized
    """
    if not workdir:
        return path

    has_sep = path[-1] == os.sep
    return_path = os.path.normpath(os.path.join(workdir, path))
    if has_sep:
        return_path += os.sep
    return return_path
