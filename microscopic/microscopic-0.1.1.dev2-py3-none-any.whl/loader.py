from functools import partial
from importlib import import_module

import pkg_resources
import yaml


class ConfigValidationError(RuntimeError):
    pass


def load_resource(group, name, *, namespace='microscopic'):
    group = '{namespace}.{group}'.format(namespace=namespace, group=group)
    for ep in pkg_resources.iter_entry_points(group, name):
        return ep.load()

    raise ImportError(group, name)


def public(config):
    for k, v in config.items():
        if not k.startswith('_'):
            yield k, v


def hack(kwargs):
    # replace import requests if they exist:
    filtered = {}
    for key, value in kwargs.items():
        if isinstance(value, dict):
            module, attr = value['__import__'].rsplit(':', maxsplit=1)
            value = getattr(import_module(module), attr)
        filtered[key] = value

    return filtered


def evaluate_config(config):
    if '__version__' not in config or config['__version__'] != '0':
        raise ConfigValidationError("__version__ is required and must be the string: '0'")

    context = {}

    for group, resource_requests in public(config):
        for context_name, resource_spec in resource_requests.items():
            if 'entry_point' not in resource_spec:
                raise ConfigValidationError(
                    "entry_point not defined for resource request: '{}'".format(context_name))

            res = load_resource(group, resource_spec['entry_point'])
            res = partial(res, *resource_spec.get('args', []), **hack(resource_spec.get('kwargs', {})))

            context_key = '{group}.{context_name}'.format(group=group, context_name=context_name)

            context[context_key] = res

    return context


def build_executor(context, config):
    # fixme: not flexible enough
    if '__executor__' not in config:
        raise ConfigValidationError("__executor__ is required")

    executor_spec = config['__executor__']

    executor_kwargs = {k: context[v] for k, v in executor_spec.items()}

    from microscopic.pipelines import pipelines
    executor = pipelines.execute_simple
    return partial(executor, **executor_kwargs)


def load_config(filename):
    with open(filename) as f:
        config = yaml.load(f)
    return config
