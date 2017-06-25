from setuptools import setup, Command, find_packages
import os
import sys

if sys.version_info < (3,0):
    sys.exit('\nSorry, Python < 3.0 is not supported\nIf you have Python 3.x installed use: pip3 install wc.py')
    sys.exit('')

currentFileDirectory = os.path.dirname(__file__)
with open(os.path.join(currentFileDirectory, "README.md"), "r") as f:
    readme = f.read()

# Maintain dependencies of requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./**/__pycache__ ./__pycache__ ./.eggs ./.cache')

print(find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]))

setup(
    name="wcpy",
    version="1.2",
    description="WordCount in Python with a lot more functionality",
    long_description=readme,
    author="Alejandro Saucedo",
    author_email="a@e-x.io",
    url="https://github.com/axsauze/wcpy",
    classifiers=[
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords="Word count (wcpy) on steroids",
    license="MIT",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=requirements,
    scripts=('wc.py',),
    data_files=[ (".", ["LICENSE"]) ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    cmdclass={
        'clean': CleanCommand
    }
)

