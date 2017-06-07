"""Coverage Environment Plugin"""
import os

from packaging.markers import default_environment

DEFAULT_ENVIRONMENT = {}


def coverage_init(reg, options):
    global DEFAULT_ENVIRONMENT
    DEFAULT_ENVIRONMENT.update([
        (k.upper(), v)
        for k, v in default_environment().items()])

    if 'markers' in options:
        os.environ.update(DEFAULT_ENVIRONMENT)
