#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="logging-slack",
    version="1.1",
    description="Logging handler for Slack Webhook",
    url="https://github.com/frrakn/logging-slack",
    author="frakn",
    author_email="cheng.frank.chen+pypi@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "slackweb==1.0.5",
    ],
    include_package_data=True,
    platform="any",
)
