"""
Auto-generated class for BankList
"""
from .BankAsset import BankAsset

from . import client_support


class BankList(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(banks):
        """
        :type banks: list[BankAsset]
        :rtype: BankList
        """

        return BankList(
            banks=banks,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'BankList'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'banks'
        val = data.get(property_name)
        if val is not None:
            datatypes = [BankAsset]
            try:
                self.banks = client_support.list_factory(val, datatypes)
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
