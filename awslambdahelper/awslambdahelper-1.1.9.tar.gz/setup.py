#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'awslambdahelper',
        version = '1.1.9',
        description = '',
        long_description = '',
        author = 'Drew J. Sonne',
        author_email = 'drew.sonne@gmail.com',
        license = 'LGLP',
        url = 'https://github.com/drewsonne/awslambdahelper',
        scripts = ['scripts/lambdahelper-bundler'],
        packages = ['awslambdahelper'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'boto3',
            'pip>=7.1',
            'setuptools~=35.0',
            'wheel'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
