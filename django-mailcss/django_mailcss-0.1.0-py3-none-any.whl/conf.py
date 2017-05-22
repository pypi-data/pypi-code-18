try:
    import importlib
except ImportError:
    from django.utils import importlib

DEFAULT_ENGINE = 'django_mailcss.engines.PynlinerEngine'


def load_class_by_path(path):
    i = path.rfind('.')
    module_path, class_name = path[:i], path[i + 1:]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def get_engine():
    from django.conf import settings
    engine_path = getattr(settings, 'MAILCSS_ENGINE', DEFAULT_ENGINE)
    return load_class_by_path(engine_path)


def get_css_loader():
    from django.conf import settings

    if settings.DEBUG:
        default_css_loader = 'django_mailcss.css_loaders.StaticFinderCSSLoader'
    else:
        default_css_loader = 'django_mailcss.css_loaders.StaticPathCSSLoader'

    engine_path = getattr(settings, 'MAILCSS_CSS_LOADER', default_css_loader)
    return load_class_by_path(engine_path)
