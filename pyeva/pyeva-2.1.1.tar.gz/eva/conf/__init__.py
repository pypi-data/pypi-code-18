"""
Settings and configuration for Eva.

from eva.conf import settings

配置读取优先级：
1. 环境变量（方便docker运行环境的配置覆盖）
2. settings.py
3. global_settings.py
"""

import logging
import os
import sys
import warnings
import importlib

from eva.conf import global_settings
from eva.exceptions import ImproperlyConfigured
from eva.utils.functional import LazyObject, empty
from eva.utils import six

ENVIRONMENT_VARIABLE = "EVA_SETTINGS_MODULE"
# FIXME!
os.environ['EVA_SETTINGS_MODULE'] = 'codebase.settings'


class LazySettings(LazyObject):
    """
    A lazy proxy for either global Django settings or a custom settings object.
    The user can manually configure settings prior to using them. Otherwise,
    Django uses the settings module pointed to by DJANGO_SETTINGS_MODULE.
    """
    def _setup(self, name=None):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        try:
            settings_module = os.environ[ENVIRONMENT_VARIABLE]
            if not settings_module:  # If it's set but is an empty string.
                raise KeyError
        except KeyError:
            desc = ("setting %s" % name) if name else "settings"
            raise ImproperlyConfigured(
                "Requested %s, but settings are not configured. "
                "You must either define the environment variable %s "
                "or call settings.configure() before accessing settings."
                % (desc, ENVIRONMENT_VARIABLE))

        self._wrapped = Settings(settings_module)
# Jian: disable this
#        self._configure_logging()

    def __getattr__(self, name):
        if self._wrapped is empty:
            self._setup(name)
        return getattr(self._wrapped, name)

    def _configure_logging(self):
        """
        Setup logging from LOGGING_CONFIG and LOGGING settings.
        """
        if not sys.warnoptions:
            try:
                # Route warnings through python logging
                logging.captureWarnings(True)
                # Allow DeprecationWarnings through the warnings filters
                warnings.simplefilter("default", DeprecationWarning)
            except AttributeError:
                # No captureWarnings on Python 2.6, DeprecationWarnings are on anyway
                pass

        if self.LOGGING_CONFIG:
            from django.utils.log import DEFAULT_LOGGING
            # First find the logging configuration function ...
            logging_config_func = import_by_path(self.LOGGING_CONFIG)

            logging_config_func(DEFAULT_LOGGING)

            # ... then invoke it with the logging settings
            if self.LOGGING:
                logging_config_func(self.LOGGING)

    def configure(self, default_settings=global_settings, **options):
        """
        Called to manually configure the settings. The 'default_settings'
        parameter sets where to retrieve any unspecified values from (its
        argument must support attribute access (__getattr__)).
        """
        if self._wrapped is not empty:
            raise RuntimeError('Settings already configured.')
        holder = UserSettingsHolder(default_settings)
        for name, value in options.items():
            setattr(holder, name, value)
        self._wrapped = holder
# Jian: disable this
#        self._configure_logging()

    @property
    def configured(self):
        """
        Returns True if the settings have already been configured.
        """
        return self._wrapped is not empty


class BaseSettings(object):
    """
    Common logic for settings whether set by a module or by the user.
    """
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)


class Settings(BaseSettings):
    def __init__(self, settings_module):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(global_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        try:
            mod = importlib.import_module(self.SETTINGS_MODULE)
        except ImportError as e:
            raise ImportError(
                "Could not import settings '%s' (Is it on sys.path? Is there an import error in the settings file?): %s"
                % (self.SETTINGS_MODULE, e)
            )

        # Settings that should be converted into tuples if they're mistakenly entered
        # as strings.
        tuple_settings = ("INSTALLED_APPS", "TEMPLATE_DIRS")

        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                if setting in tuple_settings and \
                        isinstance(setting_value, six.string_types):
                    warnings.warn("The %s setting must be a tuple. Please fix your "
                                  "settings, as auto-correction is now deprecated." % setting,
                                  DeprecationWarning, stacklevel=2)
                    setting_value = (setting_value,) # In case the user forgot the comma.
                setattr(self, setting, setting_value)

        if not self.SECRET_KEY:
            raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")


class UserSettingsHolder(BaseSettings):
    """
    Holder for user configured settings.
    """
    # SETTINGS_MODULE doesn't make much sense in the manually configured
    # (standalone) case.
    SETTINGS_MODULE = None

    def __init__(self, default_settings):
        """
        Requests for configuration variables not in this class are satisfied
        from the module specified in default_settings (if possible).
        """
        self.__dict__['_deleted'] = set()
        self.default_settings = default_settings

    def __getattr__(self, name):
        if name in self._deleted:
            raise AttributeError
        return getattr(self.default_settings, name)

    def __setattr__(self, name, value):
        self._deleted.discard(name)
        return super(UserSettingsHolder, self).__setattr__(name, value)

    def __delattr__(self, name):
        self._deleted.add(name)
        return super(UserSettingsHolder, self).__delattr__(name)

    def __dir__(self):
        return list(self.__dict__) + dir(self.default_settings)

settings = LazySettings()
