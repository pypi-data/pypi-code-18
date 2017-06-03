from types import FunctionType

from jinja2_webpack import DEFAULT_SETTINGS, Environment
from jinja2_webpack.filter import WebpackFilter
from pyramid.exceptions import ConfigurationError
from pyramid.settings import asbool
from zope.dottedname.resolve import resolve as resolve_dotted
from zope.interface import Interface


class IWebpackEnvironment(Interface):
    pass


class Jinja2EnvironmentMissingException(Exception):
    """ Thrown when configuration fails because it can't find
    the jinija2 environment """
    pass


def get_webpack_environment(context):
    return context.registry.queryUtility(IWebpackEnvironment)


def parse_multiline(val):
    result = {}
    for e in val.splitlines():
        if not e.strip():
            continue
        key, value = e.strip().split('=', 1)
        result[key] = value
    return result


def parse_renderByExt(val):
    # resolves dotted names
    result = parse_multiline(val)
    resolved_result = {}
    for k, v in result.items():
        resolved_result[k] = resolve_dotted(v)
    return resolved_result


def webpack_settings_from_settings(registry_settings, prefixes=None):
    prefixes = prefixes or ['webpack.']
    settings = {}
    for k, v in registry_settings.items():
        for prefix in prefixes:
            slicelen = len(prefix)
            if k.startswith(prefix):
                setting_name = k[slicelen:]
                try:
                    default = DEFAULT_SETTINGS[setting_name]
                except KeyError:
                    toggle = prefix + 'errorOnInvalidSetting'
                    if toggle in registry_settings:
                        default = ''
                    else:
                        raise ConfigurationError(
                            'Invalid webpack setting %s' % setting_name)
                # jinja2_webpack exposes a DEFAULT_SETTINGS dict which
                # contains the default value for all the settings.
                # Use the type of the default to process the setting from ini.
                if type(default) == bool:
                    v = asbool(v)
                elif type(default) == FunctionType:
                    v = resolve_dotted(v)
                elif setting_name == 'renderByExt':
                    v = parse_renderByExt(v)
                settings[setting_name] = v
    return settings


def includeme(config):
    registry_settings = config.registry.settings
    settings = webpack_settings_from_settings(registry_settings)
    registry_settings['webpack'] = settings

    # Load the webpack environment
    environment = Environment(**settings)
    config.registry.registerUtility(environment, IWebpackEnvironment)

    # Add callbacks
    config.add_directive('get_webpack_environment', get_webpack_environment)
    config.add_request_method(get_webpack_environment,
                              'webpack_environment', reify=True)

    # Expose a webpack filter to jinja2 environment
    webpack_filter = WebpackFilter(environment)
    try:
        jinja2_env = config.get_jinja2_environment()
    except AttributeError:
        raise Jinja2EnvironmentMissingException(
            'Unable to find jinja2 environment. '
            'Try config.commit() after including jinja2')
    jinja2_env.filters['webpack'] = webpack_filter


__version__ = '0.1.1'
