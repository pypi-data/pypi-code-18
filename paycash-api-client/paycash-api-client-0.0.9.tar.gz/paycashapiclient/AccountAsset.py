"""
Auto-generated class for AccountAsset
"""
from .AccountAssetTypes import AccountAssetTypes

from . import client_support


class AccountAsset(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(currency, enabled, id, type):
        """
        :type currency: str
        :type enabled: bool
        :type id: str
        :type type: AccountAssetTypes
        :rtype: AccountAsset
        """

        return AccountAsset(
            currency=currency,
            enabled=enabled,
            id=id,
            type=type,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'AccountAsset'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'currency'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.currency = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'enabled'
        val = data.get(property_name)
        if val is not None:
            datatypes = [bool]
            try:
                self.enabled = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'id'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.id = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'type'
        val = data.get(property_name)
        if val is not None:
            datatypes = [AccountAssetTypes]
            try:
                self.type = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
