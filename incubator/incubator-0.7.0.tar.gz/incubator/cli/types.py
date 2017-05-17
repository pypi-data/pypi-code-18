import click

from ..core.utilclasses import Volume


class KeyValue(click.ParamType):
    name = 'key=value'

    def convert(self, value, param, ctx):
        value_split = value.split('=')
        if len(value_split) != 2:
            self.fail("{} is not a valid 'key=value'.".format(value), param, ctx)
        key, value = value_split
        if not key:
            self.fail("{} is not a valid 'key=value'. (key is empty)".format(value), param, ctx)
        if not value:
            self.fail("{} is not a valid 'key=value'. (value is empty)".format(value), param, ctx)
        return key, value


class MountVolume(click.ParamType):
    name = 'volume'

    def convert(self, value, param, ctx):
        try:
            return Volume.get_instance(value)
        except ValueError as ex:
            self.fail(ex, param, ctx)


KEY_VALUE = KeyValue()
MOUNT_VOLUME = MountVolume()
