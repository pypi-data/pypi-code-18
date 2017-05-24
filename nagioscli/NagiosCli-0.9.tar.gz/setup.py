#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name = "NagiosCli",
    version = "0.9",
    packages = find_packages(),
    scripts = ['nagios_cli.py', 'template.txt', 'function_map.py', 'ldapVerify.py', 'ldapAuth.py', 'printf'],
    install_requires = ['docutils>=0.3'],

    # metadata for upload to PyPI
    author = "instart/ops",
    author_email = "sanusha@instartlogic.com",
    url = "https://opsgerrit.vpn.insnw.net/#/admin/projects/ops/scripts2",
    description = "CLI for bulk alert management",
)
