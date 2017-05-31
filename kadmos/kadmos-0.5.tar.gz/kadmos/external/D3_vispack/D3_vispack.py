import shutil
import os
import re


def D3_vispack_version():
    """Function returns most recent visualization package version"""

    search_path = os.path.dirname(os.path.abspath(__file__))
    all_subdirs = [name for name in os.listdir(search_path) if os.path.isdir(os.path.join(search_path, name))]
    all_versions = [re.findall('\d+', version) for version in all_subdirs]
    version = str(max(all_versions)[0])

    return version


def D3_vispack_copy(new_folder_name, vispack_version=D3_vispack_version()):
    """
    Function to copy a version of the visualization package to a new subfolder.

    :param new_folder_name: name of the folder to put the visualization package
    :type new_folder_name: basestring
    :param vispack_version: version of the visualization package in yymmdd format
    :type vispack_version: basestring
    :return: folder with visualization package
    :rtype: file
    """

    # Get folder of D3_vispack package
    vispack_folder = 'KADMOS_VisualizationPackage_' + vispack_version

    # Copy and rename folder
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), vispack_folder)
    dst = os.path.join(os.getcwd(), new_folder_name)

    if os.path.isdir(dst):
        shutil.rmtree(dst)

    shutil.copytree(src, dst)
