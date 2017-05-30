'''Zip Downloader'''

import zipfile
import os
import shutil
from urllib.request import urlretrieve
from buildsystem.builder import Builder, task


class ZipDependencyResolver(Builder):
    '''
    self.deps needs to be an array of dictionaries with the following keys:
        - url: url to download the file from
        - dirname: directory name to extract contents to
    '''
    depdir = 'deps'
    deps = []

    @task('deps')
    def dependencies(self):
        '''Downloads and extracts the dependencies defined in self.deps'''
        shutil.rmtree(self.depdir)

        for dep in self.deps:
            urlretrieve(dep['url'], 'tmp.zip')
            zfile = zipfile.ZipFile('tmp.zip')
            zfile.extractall(os.path.join(self.depdir, dep['dirname']))
            zfile.close()
            os.remove('tmp.zip')
