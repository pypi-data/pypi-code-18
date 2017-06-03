#!/usr/bin/env python
__author__ = 'Daniel Alexander Ross Evans'

import os
import simplejson as json
import shutil
import sys
import fire
from collections import defaultdict
from pkg_resources import resource_string

ext = resource_string(__name__, "extensions.json")
extensions = json.loads(ext)

def path_to_folder(path):
    """Finds the right-most forward-slash and returns all characters to the right of it"""
    return str(path[path.rfind("/")+1:])


def filetype(path, withPeriod=False):
    """Finds the right-most period and returns all characters to the right of it"""
    if withPeriod:
        return os.path.splitext(path)[1]
    else:
        return os.path.splitext(path)[1][1:]


def get_files(path, levels=-1):
    """Checks files and folders, searches subfolders recursively"""
    files = {path_to_folder(path):[]}
    for filename in os.listdir(path):
        try:
            # if this errors, then this is a file
            os.listdir(path + "/" + filename)
            # if it doesn't error, this is a Folder
            # check that the folder is not a Folder we tend to sort into
            if filename not in extensions.keys():
                if levels > 0:
                    # if this passes we are searching the files of this folder
                    files[filename] = {}
                    print("Searching Folder:", (filename))
                    files[filename] = get_files(path + "/" + filename, levels-1)
        except OSError:
            # add file to dictionary
            files[path_to_folder(path)].append(path + "/" + filename)
    print("Leaving Folder:", path_to_folder(path))
    return files


def sort_by_filetype(files, rPath):
    """Moves files into new folders, handles folders recursively"""
    moving_files = defaultdict(list)
    folders_to_sort = []
    for folder in files:
        if isinstance(files[folder], list):
            # if instance has files, prepare for sorting
            for a_file in files[folder]:
                moving_files[filetype(a_file)].append(a_file)
        if isinstance(files[folder], dict):
            # if instance is folder, sort the folder
            folders_to_sort.append(folder)
    for item in moving_files.keys():
        if isinstance(moving_files[item], list):
            final_destination = ""
            try:
                for folder in extensions:
                    if str(item).lower() in extensions[folder]:
                        final_destination = rPath + "/" + folder
                        os.mkdir(final_destination)
                        break
            except OSError:
                pass

            for the_file in moving_files[item]:
                try:
                    for folder_name in extensions:
                        if str(item).lower() in extensions[folder_name]:
                            print("File:", path_to_folder(the_file))
                            final_destination = rPath + "/" + folder_name + "/"  + path_to_folder(the_file)
                            print("Moving to", (final_destination))
                            shutil.move(the_file, final_destination)
                            print("Moved to", (final_destination))
                            break

                except shutil.Error:
                    pass
        for folder in folders_to_sort:
            sort_by_filetype(files[folder], rPath + "/" + folder)

def organize(path=os.getcwd(), levels=0):
    sort_by_filetype(get_files(path=path, levels=levels), path)

def main():
    fire.Fire(organize)

if __name__ == '__main__':
    main()
