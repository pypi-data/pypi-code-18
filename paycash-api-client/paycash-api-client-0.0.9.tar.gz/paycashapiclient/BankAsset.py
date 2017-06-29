"""
Auto-generated class for BankAsset
"""

from . import client_support


class BankAsset(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(bic, country, currency, enabled, holder, id, institute, mandateDate, mandateRef, verified):
        """
        :type bic: str
        :type country: str
        :type currency: str
        :type enabled: bool
        :type holder: str
        :type id: str
        :type institute: str
        :type mandateDate: str
        :type mandateRef: str
        :type verified: bool
        :rtype: BankAsset
        """

        return BankAsset(
            bic=bic,
            country=country,
            currency=currency,
            enabled=enabled,
            holder=holder,
            id=id,
            institute=institute,
            mandateDate=mandateDate,
            mandateRef=mandateRef,
            verified=verified,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'BankAsset'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'bic'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.bic = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'country'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.country = client_support.val_factory(val, datatypes)
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

        property_name = 'holder'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.holder = client_support.val_factory(val, datatypes)
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

        property_name = 'institute'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.institute = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'mandateDate'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.mandateDate = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'mandateRef'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.mandateRef = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'verified'
        val = data.get(property_name)
        if val is not None:
            datatypes = [bool]
            try:
                self.verified = client_support.val_factory(val, datatypes)
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
