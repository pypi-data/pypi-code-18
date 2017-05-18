"""
Auto-generated class for CreateBankReqBody
"""

from . import client_support


class CreateBankReqBody(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(bic, country, currency, iban, institute, mandate):
        """
        :type bic: str
        :type country: str
        :type currency: str
        :type iban: str
        :type institute: str
        :type mandate: bool
        :rtype: CreateBankReqBody
        """

        return CreateBankReqBody(
            bic=bic,
            country=country,
            currency=currency,
            iban=iban,
            institute=institute,
            mandate=mandate,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'CreateBankReqBody'
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

        property_name = 'iban'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.iban = client_support.val_factory(val, datatypes)
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

        property_name = 'mandate'
        val = data.get(property_name)
        if val is not None:
            datatypes = [bool]
            try:
                self.mandate = client_support.val_factory(val, datatypes)
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
