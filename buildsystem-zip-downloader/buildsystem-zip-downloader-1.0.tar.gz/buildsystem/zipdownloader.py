'''Zip Downloader'''

from urllib.request import urlretrieve
import zipfile
import os
import shutil
from buildsystem.packager import BaseBuilder, task


class ZipDependencyResolver(BaseBuilder):
    '''
    self.deps needs to be an array of dictionaries with the following keys:
        - url: url to download the file from
        - dirname: directory name to extract contents to
    '''
    depdir = 'deps'
    deps = []

    @task('deps')
    def dependencies(self):
        shutil.rmtree(self.depdir)

        for dep in self.deps:
            urlretrieve(dep['url'], 'tmp.zip')
            zf = zipfile.ZipFile('tmp.zip')
            zf.extractall(os.path.join(self.depdir, dep['dirname']))
            zf.close()
            os.remove('tmp.zip'
