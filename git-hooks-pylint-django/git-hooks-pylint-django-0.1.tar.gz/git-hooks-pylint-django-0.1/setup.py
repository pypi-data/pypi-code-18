import os
import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install

pylint_check_code = """#!/usr/bin/env python

import argparse
import sys
import os
from os.path import dirname

import django
from pylint.lint import Run


def run_pylint():
    # Runs Pylint on codebase and updates with status of files
    from django.conf import settings
    if sys.version_info >= (3, 4):
        import importlib
        importlib.reload(django.conf)
    elif sys.version_info >= (3, 0):
        import imp
        imp.reload(django.conf)
    else:
        reload(module)
    from django.conf import settings

    results = Run(['--load-plugins=pylint_django', '--rcfile=pylintrc', settings.CODEBASE], exit=False)
    if results.linter.stats['error'] > settings.ERROR_COUNT or \
        results.linter.stats['convention'] > settings.CONVENTION_COUNT or \
        results.linter.stats['warning'] > settings.WARNINGS or \
        results.linter.stats['global_note'] < settings.THRESHOLD_LINT_SCORE:
        print("Codebase has failed set standards, Please correct above mentioned issues before commit,"
              "Current Score is: %s, Errors: %s, Convention issues: %s, Warnings: %s" % (\
            results.linter.stats['global_note'], results.linter.stats['error'], results.linter.stats['convention'],
            results.linter.stats['warning']))
        os._exit(1)

def main():
    SITE_ROOT = dirname(dirname(dirname(dirname(os.path.dirname(os.path.realpath(__file__))))))
    sys.path.append(SITE_ROOT)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.conf.settings")
    run_pylint()


if __name__ == "__main__":
    main()
"""

class GitHookSetup(install):
    """
        class GitHookSetup
        Has a run method which check presence of pre-commit hook of git,
        if already present removes it, else creates a new one using the content present in 
        "pylint_check_code" string. Also update the permission of file as required.
    """

    def run(self):
        install.run(self)

        # Remove if pre-commit hook if exists any
        try:
            os.remove('.git/hooks/pre-commit')
        except:
            print ('No existing pre commit hook found')
            pass

        f = open('.git/hooks/pre-commit', 'w+')
        f.write(pylint_check_code)
        f.close()
        subprocess.call(['chmod', '0755', '.git/hooks/pre-commit'])


setup(
    name='git-hooks-pylint-django',
    version='0.1',
    packages=find_packages(),
    description='Git hooks for pylint, for django projects',
    long_description='Currently adds pre-commit hook to git codebase, which runs pylint over the given django codebase',

    # The project's main homepage.
    url='https://github.com/saurabhprakash/git-hooks-pylint-django',
    download_url = 'https://codeload.github.com/saurabhprakash/git-hooks-pylint-django/zip/master', 
    keywords = ['Django', 'pylint'], # arbitrary keywords
    # Author details
    author='Saurabh',
    author_email='saurabhpresent@gmail.com',
    # install_requires=[
    #     'pylint>=1.5',
    # ],
    cmdclass={'install': GitHookSetup},
    # entry_points={
    #     'console_scripts': [
    #         'core=core:main',
    #     ],
    # },
)
