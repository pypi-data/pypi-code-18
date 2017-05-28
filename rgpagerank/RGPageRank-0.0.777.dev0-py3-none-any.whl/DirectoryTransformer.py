from os import listdir
from os import path
from os import getcwd
from collections import OrderedDict

from RGPageRank.BaseTransformer import BaseTransformer


class DirectoryTransformer(BaseTransformer):

    """
    get data from the dir recursively or not
    """
    __recursive = False

    """
    truncate extension from nodes
    """
    __truncate_extension = True

    """
    current directory
    """
    __dir_path = ''

    """
    gather all errors during extracting data
    """
    errors = {}

    def __init__(self, dir_name, recursive=False, truncate_extension=True):

        self.__recursive = recursive
        self.__truncate_extension = truncate_extension
        self.__dir_path = getcwd()

        BaseTransformer.__init__(self, dir_name)

    def prepare(self, data):

        dir_name = self.resolve_dir_name(data)

        if not path.isdir(dir_name):
            raise IsADirectoryError('The directory "{dir}" does not exists'.format(dir=dir_name))

        return self.extract_data(dir_name)

    def extract_data(self, dir_name):

        dir_data = OrderedDict([])

        for file_name in listdir(dir_name):

            file_path = dir_name + path.sep + file_name

            if path.isdir(file_path):
                if self.__recursive:
                    dir_data = self.merge_dicts(dir_data, self.extract_data(file_path))
                else:
                    self.errors[file_name] = 'File name {name} is actually a directory'.format(name=file_name)
                continue

            try:
                if file_name not in dir_data:
                    if self.__truncate_extension:
                        dir_data[file_name[0:file_name.rfind('.')]] = open(file_path, 'r').read()
                    else:
                        dir_data[file_name] = open(file_path, 'r').read()
            except Exception as e:
                self.errors[e] = str(e)

        return dir_data

    def resolve_dir_name(self, dir_name):
        if not dir_name:
            return self.__dir_path

        if isinstance(dir_name, str) and (dir_name.find(':\\') == 1 or dir_name.find('/') == 0):
            return dir_name

        return self.__dir_path + path.sep + str(dir_name).lstrip(path.sep)

    @staticmethod
    def merge_dicts(dict1, dict2):

        for k, v in dict2.items():
            dict1[k] = dict1[k] + ' ' + v if k in dict1 else v

        return dict1
