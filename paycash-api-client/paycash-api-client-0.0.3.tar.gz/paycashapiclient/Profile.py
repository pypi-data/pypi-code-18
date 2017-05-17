"""
Auto-generated class for Profile
"""
from .Address import Address
from .Email import Email
from .KYC import KYC
from .Work import Work

from . import client_support


class Profile(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(addresses, birthDate, emails, firstName, id, kyc, language, lastName, salutation, verificationLevel, work=None):
        """
        :type addresses: list[Address]
        :type birthDate: str
        :type emails: list[Email]
        :type firstName: str
        :type id: str
        :type kyc: list[KYC]
        :type language: str
        :type lastName: str
        :type salutation: str
        :type verificationLevel: str
        :type work: Work
        :rtype: Profile
        """

        return Profile(
            addresses=addresses,
            birthDate=birthDate,
            emails=emails,
            firstName=firstName,
            id=id,
            kyc=kyc,
            language=language,
            lastName=lastName,
            salutation=salutation,
            verificationLevel=verificationLevel,
            work=work,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'Profile'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'addresses'
        val = data.get(property_name)
        if val is not None:
            datatypes = [Address]
            try:
                self.addresses = client_support.list_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'birthDate'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.birthDate = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'emails'
        val = data.get(property_name)
        if val is not None:
            datatypes = [Email]
            try:
                self.emails = client_support.list_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'firstName'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.firstName = client_support.val_factory(val, datatypes)
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

        property_name = 'kyc'
        val = data.get(property_name)
        if val is not None:
            datatypes = [KYC]
            try:
                self.kyc = client_support.list_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'language'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.language = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'lastName'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.lastName = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'salutation'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.salutation = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'verificationLevel'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.verificationLevel = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'work'
        val = data.get(property_name)
        if val is not None:
            datatypes = [Work]
            try:
                self.work = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
