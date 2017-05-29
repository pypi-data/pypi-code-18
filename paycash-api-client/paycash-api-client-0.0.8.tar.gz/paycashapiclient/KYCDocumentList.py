"""
Auto-generated class for KYCDocumentList
"""

from . import client_support


class KYCDocumentList(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(billingAddress=None, cardId=None, drivingLicense=None, legalEntityIdentifier=None, passport=None, personalIdentity=None):
        """
        :type billingAddress: str
        :type cardId: str
        :type drivingLicense: str
        :type legalEntityIdentifier: str
        :type passport: str
        :type personalIdentity: str
        :rtype: KYCDocumentList
        """

        return KYCDocumentList(
            billingAddress=billingAddress,
            cardId=cardId,
            drivingLicense=drivingLicense,
            legalEntityIdentifier=legalEntityIdentifier,
            passport=passport,
            personalIdentity=personalIdentity,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'KYCDocumentList'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'billingAddress'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.billingAddress = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'cardId'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.cardId = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'drivingLicense'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.drivingLicense = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'legalEntityIdentifier'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.legalEntityIdentifier = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'passport'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.passport = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'personalIdentity'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.personalIdentity = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
