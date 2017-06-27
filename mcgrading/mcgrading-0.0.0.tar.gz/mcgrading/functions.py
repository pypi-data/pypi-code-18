import os
from glob import glob
from shutil import rmtree
from zipfile import ZipFile
from importlib.machinery import SourceFileLoader

CURRENT_DIRECTORY = os.getcwd()

def getZipFiles():
    return glob("*.zip")

def getTxtFiles():
    return glob("*.txt")

def cleanFiles(names):
    for name in names:
        try:
            os.remove(name)
        except Exception as e:
            print(e)

def importFile(module):
    loader = SourceFileLoader(module, '%s.py'%module)
    return loader.load_module()

def convert2to3(file_name):
    os.system("2to3 -w %s"%file_name)

def fileExists(file):
    return os.path.isfile(file)

def cleanMACOS():
    rmtree('__MACOSX')
