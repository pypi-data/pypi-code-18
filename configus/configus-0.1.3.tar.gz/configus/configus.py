import os
import sys
import warnings

import trafaret

DefaultEnvFile = '.env'


def config(schema, env=None, ignore_extra=True, config_file=DefaultEnvFile):
    """
    Verifies env data by passed schema.

    Args:
        schema: trafaret schema
        env: dictionary like object or None (os.environ will be used)
        ignore_extra: ignore extra parameters in env
        config_file: envfile path
    Returns:
        verified data
    """

    assert isinstance(schema, trafaret.Trafaret), "Unexpected schema"
    all_upper = False
    if isinstance(schema, trafaret.Dict):
        keys = schema.keys
        names = [k.get_name() for k in keys]
        all_upper = all(map(lambda s: s.isupper(), names))
    env = env or os.environ.copy()
    if ignore_extra:
        schema = schema.ignore_extra('*')

    envfile = maybe_read_envfile(config_file)

    _env = envfile.copy()
    _env.update(**env)
    agrs_env = maybe_get_argv()
    _env.update(**agrs_env)
    duplicates = _check_dup_keys(hs_map=_env)

    if duplicates:
        warnings.warn('Duplicate keys in different case found! {}'.format(duplicates))
    if not all_upper:
        _env = {k.lower(): v for k, v in _env.items()}
    return schema.check(_env)


def config_with_error(schema, env=None, ignore_extra=True, **opt):
    try:
        data = config(schema, env=None, ignore_extra=True, **opt)
    except trafaret.DataError as e:
        return None, e
    return data, None


def maybe_get_argv(argv=()):
    vars = {}
    argv = argv or sys.argv[1:]
    for arg in argv:
        # todo: make more posix compliant argv parsing
        parts = arg.split('=')
        if len(parts) != 2:
            continue
        key, val = parts[0], parts[1]
        key = key.strip('-')
        vars[key] = val
    return vars


def maybe_read_envfile(file_name):
    if not os.path.exists(file_name):
        if file_name == DefaultEnvFile or not file_name:
            return {}
        raise EnvironmentError('Passed envfile does not exists {}'.format(file_name))

    with open(file_name, 'r') as efile:
        content = efile.readlines()
    return parse_envfile(content)


def parse_envfile(lines):
    vars = {}
    for expression in lines:
        expression = expression.strip('\t\n ')
        if not expression:
            continue
        if expression.startswith('export'):
            expression = expression[6:]

        parts = expression.split('=')
        if len(parts) != 2:
            continue
        key, val = parts[0].strip(), parts[1].strip()
        if not key:
            continue
        vars[key] = val
    return vars


def _check_dup_keys(hs_map):
    dups = []
    for k in hs_map:
        if k.upper() in hs_map:
            dups.append((k, k.upper()))
    return dups
