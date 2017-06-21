import logging

import jinja2

LOGGER = logging.getLogger(__name__)

STATE = {
    'env'   : None,
}

class TemplateError(Exception):
    pass

def set_environment(templates_path):
    env = jinja2.Environment(
        loader = jinja2.FileSystemLoader(templates_path),
    )
    STATE['env'] = env

def render(templatename, **kwargs):
    env = STATE['env']
    if not env:
        raise TemplateError("Your environment does not support template rendering")
    template = STATE['env'].get_template(templatename)
    return template.render(**kwargs)
