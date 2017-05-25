
from lawes.conf import global_settings
import importlib
import os
from lawes.core.exceptions import ImproperlyConfigured

ENVIRONMENT_VARIABLE = "LAWES_SETTINGS_MODULE"

class LazySettings(object):

    _wrapped = None

    def _setup(self, name=None):

        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            desc = ("setting %s" % name) if name else "settings"
            raise ImproperlyConfigured(
                "Requested %s, but settings are not configured. "
                "You must either define the environment variable %s "
                "before accessing settings."
                % (desc, ENVIRONMENT_VARIABLE))
        self._wrapped = Settings(settings_module)

    def __getattr__(self, name):
        if not self._wrapped:
            self._setup(name)
        return getattr(self._wrapped, name)

class BaseSettings(object):

    def __setattr__(self, name, value):
        if name in ("MEDIA_URL", "STATIC_URL") and value and not value.endswith('/'):
            raise ImproperlyConfigured("If set, %s must end with a slash" % name)
        object.__setattr__(self, name, value)

class Settings(BaseSettings):

    def __init__(self, settings_module):
        # update this dict from global settings
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))
        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module
        mod = importlib.import_module(self.SETTINGS_MODULE)
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

settings = LazySettings()
