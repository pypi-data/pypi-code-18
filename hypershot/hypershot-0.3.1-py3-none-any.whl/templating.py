""" Hypershot Jinja2 Templating.
"""
import io
import os
import re
import glob
import json
import collections
import pkg_resources

import yaml
import jinja2

from . import util


def load(name, builtin_only=False):
    """ Load the text of a Jinja2 template named ``name``.

        ``name`` can also point to an existing template file at any location.
    """
    from .config import config_dir, log

    if builtin_only:
        template_file = None
    elif os.path.exists(name):
        template_file = name
    elif os.sep in name:
        raise ValueError('Cannot find template file "{}"'.format(name))
    else:
        template_file = os.path.join(config_dir, name + '.j2')

    if template_file and os.path.exists(template_file):
        log.debug('Opening template "%s"', template_file)
        with io.open(template_file, encoding='utf-8') as handle:
            text = handle.read()
    else:
        try:
            text = pkg_resources.resource_string(__name__.split('.')[0],
                                                 'data/templates/{}.j2'.format(name))
            text = text.decode('utf-8')
        except FileNotFoundError as cause:
            log.debug('Cannot find template resource "%s": %s', name, cause)
            text = None
        if not text:
            raise ValueError('Cannot find template with name "{}"'.format(name))

    log.debug('Template text:\n%s', text)
    return text


def _j2utils():
    """Return Jinja2 utility namespace, and custom filters."""
    @jinja2.contextfunction
    def get_context(context):
        'Jinja2 context helper.'
        return context

    @jinja2.contextfunction
    def get_namespace(context):
        'Jinja2 namespace helper.'
        return {key: val
                for key, val in context.parent.items()
                if key not in {'u'}
                and not callable(val)
               }

    @jinja2.contextfilter
    def mask_secrets(context, text):
        'Filter for hiding secrets.'
        password = context.parent.get('settings', {}).get('password')
        return text.replace(password, '?' * len(password)) if password else text

    utils = dict(
        context=get_context,
        namespace=get_namespace,
    )
    filters = dict(
        json=lambda _: json.dumps(_, indent=4, sort_keys=True, cls=util.SmartJSONEncoder),
        mask_secrets=mask_secrets,
        re_sub=lambda _, regex, repl: re.sub(regex, repl, _),
        repr=repr,
        yaml=yaml.dump,
    )
    return utils, filters


def render(name, namespace):
    """Render the Jinja2 template named ``name`` and the given ``namespace``."""
    utils, filters = _j2utils()
    j2loader = jinja2.FunctionLoader(load)
    j2env = jinja2.Environment(autoescape=False, loader=j2loader)
    j2env.filters.update(filters)

    tmpl = j2env.get_template(name)
    return tmpl.render(collections.ChainMap(dict(u=utils), namespace))


def inventory():
    """Generate a ``(name, description)`` tuple for all templates, built-in and custom ones alike."""
    from .config import config_dir

    def description(name, path=None):
        'Helper to load description'
        text = load(path or name, builtin_only=path is None)
        if text.startswith('{#'):
            return text.split('\n', 1)[0].lstrip('{').rstrip('}').strip('#').strip()
        elif path:
            return util.pretty_path(path)
        else:
            return 'Built-in template'  # pragma: no cover

    # Do built-in ones first, so if fed into a dict() constructor custom ones win
    for name in pkg_resources.resource_listdir(__name__.split('.')[0], 'data/templates'):
        if name.endswith('.j2'):
            name = name[:-3]
            yield name, description(name)

    for path in glob.glob(os.path.join(config_dir, '*.j2')):
        name, _ = os.path.splitext(os.path.basename(path))
        yield name, description(name, path)
