"""
Auto-generated class for CreateProfileReqBody
"""
from .Address import Address
from .Work import Work

from . import client_support


class CreateProfileReqBody(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(address, birthDate, firstName, language, lastName, salutation, work):
        """
        :type address: Address
        :type birthDate: str
        :type firstName: str
        :type language: str
        :type lastName: str
        :type salutation: str
        :type work: Work
        :rtype: CreateProfileReqBody
        """

        return CreateProfileReqBody(
            address=address,
            birthDate=birthDate,
            firstName=firstName,
            language=language,
            lastName=lastName,
            salutation=salutation,
            work=work,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'CreateProfileReqBody'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'address'
        val = data.get(property_name)
        if val is not None:
            datatypes = [Address]
            try:
                self.address = client_support.val_factory(val, datatypes)
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

        property_name = 'work'
        val = data.get(property_name)
        if val is not None:
            datatypes = [Work]
            try:
                self.work = client_support.val_factory(val, datatypes)
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
