"""Setup script for setuptools-antlr."""
import sys

import setuptools

# need to guard script here due to reentrance while testing multiprocessing:
if __name__ == '__main__':
    if sys.version_info < (3, 5):
        print('This Python version isn\'t supported, minimal version 3.5 is required.')
        exit(1)

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner_opt = ['pytest-runner>=2.0,<3dev'] if needs_pytest else []

    needs_pylint = {'lint'}.intersection(sys.argv)
    setuptools_lint_opt = ['setuptools-lint>=0.4,<0.5dev'] if needs_pylint else []

    needs_flake8 = {'flake8'}.intersection(sys.argv)
    flake8_opt = ['flake8>=2.0,<3dev', 'flake8-import-order>=0.9,<0.10dev',
                  'flake8-todo>=0.5,<0.6dev', 'pep8-naming>=0.3,<0.4dev'] if needs_flake8 else []

    setuptools.setup(
        name='setuptools-antlr',
        version='0.0.6',
        packages=setuptools.find_packages(),
        package_data={'setuptools_antlr': ['lib/antlr-4.6-complete.jar', 'lib/LICENSE.txt']},
        entry_points={
            'distutils.commands': [
                'antlr = setuptools_antlr.command:AntlrCommand'
            ]
        },
        tests_require=[
            'pytest-cov'
        ],
        setup_requires=pytest_runner_opt + setuptools_lint_opt + flake8_opt,
        url='https://github.com/ferraith/setuptools-antlr',
        license='MIT',
        author='Andreas Schmidl',
        author_email='Andreas.Schmidl@gmail.com',
        description='Setuptools command for generating ANTLR based parsers.',
        platforms=[
            'any'
        ],
        keywords='antlr setuptools dsl',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ]
    )
