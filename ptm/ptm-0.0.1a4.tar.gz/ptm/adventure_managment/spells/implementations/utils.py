'''
Module contains secondary functions for spells.
'''
from os import makedirs
from os.path import exists, join, isdir


def make_package(package_path: str):
    '''
    Create python package with package_path path.
        :param package_path: path of new package
        :type package_path: string
    '''
    if not exists(package_path) or not isdir(package_path):
        makedirs(package_path)
        make_module(join(package_path, '__init__.py'))


def make_module(module_path: str):
    '''
    Create python module.
        :param module_path: path of new module
        :type module_path: string
    '''
    if not exists(module_path):
        with open(module_path, 'w+'):
            pass


def apply(function, iterator):
    '''
    Apply function for all values from iterator.
    '''
    for value in iterator:
        function(value)
