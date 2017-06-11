"""This file will have all the utilities to create the new tool setup."""

import os


class Tooler(object):
    """Tooler Module to start with."""

    def __init__(self):
        """Constructor to start with."""
        pass

    def mkdir(self, path):
        os.mkdir(path)

    def mkpkg(self, name):
        self.pkg = name
        self.mkdir(name)
        self.mkdir(os.path.join(name, 'tests'))
        self.mkdir(os.path.join(name, name))

        with open(os.path.join(name, name, '__init__.py'), 'w') as f:
            f.write('')

        for item in [
                'setup.py', 'requirements.txt', 'test-requirements.txt',
                'README.rst', '.gitignore']:
            with open(os.path.join(name, item), 'w') as f:
                f.write('')

        self._prepare_gitignore()
        self._prepare_setup()

    def _prepare_gitignore(self):
        with open(os.path.join(self.pkg, '.gitignore'), 'w') as f:
            f.write('*.pyc')

    def _prepare_setup(self):
        author_name = raw_input('Provide Author name for the tool: ')
        author_email = raw_input('Provide Author email for the tool: ')

        with open(os.path.join(self.pkg, 'setup.py'), 'w') as f:
            f.write("""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    # Filter comments
    lines = (x.strip() for x in f.readlines() if x.strip()[0] != '#')
    # Filter non -i/-r lines
    install_requires = [x for x in lines if x[0] != '-']

with open('test-requirements.txt', 'r') as f:
    # Filter comments
    lines = (x.strip() for x in f.readlines() if x.strip()[0] != '#')
    # Filter non -i/-r lines
    test_requires = [x for x in lines if x[0] != '-']


setup(name='{pkg}',
      description='Short description of the tool.',
      long_description='''
Long Description of the tool.
''',
      keywords='',
      author='{author}',
      author_email='{email}',
      license='License of the tool',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: Other/Proprietary License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7, 3.5',
          'Operating System :: OS Independent',
      ],
      packages=find_packages(exclude=("test",)),
      include_package_data=True,
      install_requires=install_requires,
      setup_requires=['tcversioner'],
      tcversioner={{
          'version_module_paths': ['{pkg}/_version.py'],
          'use_dev_not_post': True,
      }},
      test_suite='nose.collector',
      extras_require={{
          'tests': test_requires,
      }},
)
""".format(pkg=self.pkg, author=author_name, email=author_email))


if __name__ == '__main__':
    t = Tooler()
    t.mkpkg('test-tool')
