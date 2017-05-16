
import attr

import logging_helper
from _metadata import __version__, __authorshort__, __module_name__
from resources import templates, schema
from configurationutil import Configuration, cfg_params, CfgItems, CfgItem
from networkutil.endpoint_config import Endpoints

logging = logging_helper.setup_logging()

# Register Config details (These are expected to be overwritten by an importing app)
cfg_params.APP_NAME = __module_name__
cfg_params.APP_AUTHOR = __authorshort__
cfg_params.APP_VERSION = __version__

# Set the config initialisation parameters
DEVICE_CONFIG = u'device_config'

TEMPLATE = templates.devices
SCHEMA = schema.devices


# Device property keys
@attr.s(frozen=True)
class _DeviceConstant(object):
    name = attr.ib(default=u'name', init=False)
    ip = attr.ib(default=u'ip', init=False)
    port = attr.ib(default=u'port', init=False)
    active = attr.ib(default=u'active', init=False)
    default = attr.ib(default=u'default', init=False)

DeviceConstant = _DeviceConstant()


def _register_device_config():

    # Retrieve configuration instance
    cfg = Configuration()

    # Register configuration
    cfg.register(config=DEVICE_CONFIG,
                 config_type=cfg_params.CONST.json,
                 template=TEMPLATE,
                 schema=SCHEMA)

    return cfg


class Device(CfgItem):

    def __init__(self,
                 **parameters):
        super(Device, self).__init__(**parameters)

    def get_endpoint(self,
                     api,
                     environment):
        return Endpoints().get_endpoint(api=api,
                                        environment=self.__dict__[environment])


class Devices(CfgItems):

    def __init__(self):
        super(Devices, self).__init__(cfg_fn=_register_device_config,
                                      cfg_root=DEVICE_CONFIG,
                                      key=DeviceConstant.name,
                                      has_active=DeviceConstant.active,
                                      item_class=Device)

    def get_default_device(self):

        default = [device for device in self.get_items() if device.default]

        if len(default) == 1:
            return default[0]

        elif len(default) == 0:
            # If we get to here no default device is configured
            self._set_first_configured_device_as_default()
            return self.get_default_device()

        else:
            raise LookupError(u'More than one default Device is configured!')

    def get_default_device_or_first_configured(self):

        """
        Attempts to retrieve the default device.
        If no default device configured then it will return the first active device.
        If no active devices then it will return the first device it can get!
        """

        try:
            return self.get_default_device()

        except LookupError:

            try:
                return self.get_active_items()[0]

            except IndexError:
                return self.get_items()[0]

    def _set_first_configured_device_as_default(self):

        devices = self.get_items()

        device = devices[0]
        device.default = True
        device.save_changes()

        for device in devices[1:]:
            device.default = False
            device.save_changes()
