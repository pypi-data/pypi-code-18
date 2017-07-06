import os
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession


def get_requirements():
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_file):
        requirements = parse_requirements(
            os.path.join(os.path.dirname(__file__), "requirements.txt"),
            session=PipSession())
        return [str(req.req) for req in requirements]
    return []


def get_version():
    __version__ = None
    with open('needinit/_version.py') as version_src:
        exec(version_src.read())
    return __version__

setup(
    name='needinit',
    version=get_version(),
    description='Prevent callability on un-initialized objects',
    url='https://github.com/steinnes/needinit',
    author='Steinn Eldjarn Sigurdarson',
    author_email='steinnes@gmail.com',
    keywords=['library', 'object initialization'],
    install_requires=get_requirements(),
    packages=find_packages(),
)
