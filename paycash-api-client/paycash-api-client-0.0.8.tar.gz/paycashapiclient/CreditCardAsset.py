"""
Auto-generated class for CreditCardAsset
"""

from . import client_support


class CreditCardAsset(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(brand, currency, expiry, id, lastNumbers):
        """
        :type brand: str
        :type currency: str
        :type expiry: bool
        :type id: str
        :type lastNumbers: str
        :rtype: CreditCardAsset
        """

        return CreditCardAsset(
            brand=brand,
            currency=currency,
            expiry=expiry,
            id=id,
            lastNumbers=lastNumbers,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'CreditCardAsset'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'brand'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.brand = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

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

        property_name = 'expiry'
        val = data.get(property_name)
        if val is not None:
            datatypes = [bool]
            try:
                self.expiry = client_support.val_factory(val, datatypes)
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

        property_name = 'lastNumbers'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.lastNumbers = client_support.val_factory(val, datatypes)
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
