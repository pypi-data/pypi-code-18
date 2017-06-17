#!/usr/bin/env python

from setuptools import setup

setup(
    name='ansible-test-tool',
    version='1.0.0',
    description='An ansible testing framework',
    author='Lukas Beumer',
    author_email='lukas@familie-beumer.de',
    include_package_data=True,
    url='https://github.com/Nitaco/ansible-test.git',
    download_url='https://github.com/peterldowns/mypackage/archive/1.0.0.tar.gz',
    packages=['ansible_test'],
    package_data={
        "ansible_test": [
            "resources/ansible.cfg.j2",
            "resources/Dockerfile.j2",
            "resources/inventory.ini"]
    },
    scripts=['bin/ansible-test'],
    install_requires=['Jinja2', 'MarkupSafe', 'GitPython'],
    keywords=['testing', 'ansible', 'framework', 'roles'],
    classifiers=[],
)
