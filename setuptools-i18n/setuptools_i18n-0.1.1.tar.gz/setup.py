from setuptools import setup

import setuptools_i18n


def main():
    setup(name='setuptools_i18n',
          version=setuptools_i18n.__version__,
          description='Plugin for setuptools to build and compile i18n files',
          long_description=open('README.md').read(),
          py_modules=['setuptools_i18n'],
          author='Tomas Pazderka',
          author_email='tomas.pazderka@nic.cz',
          url='https://github.com/CZ-NIC/setuptools_i18n',
          entry_points={
              "distutils.commands": [
                  "build_i18n = setuptools_i18n:build_i18n",
              ],
              "distutils.setup_keywords": [
                  "i18n_files = setuptools_i18n:validate_i18n",
              ],
          },
          license='GPLv3',
          classifiers=[
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Topic :: Software Development :: Build Tools',
          ],
          )


if __name__ == '__main__':
    main()
