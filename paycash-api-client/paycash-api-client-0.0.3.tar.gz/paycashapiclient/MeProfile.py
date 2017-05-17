"""
Auto-generated class for MeProfile
"""

from . import client_support


class MeProfile(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(birthDate=None, firstName=None, lastName=None, salutation=None):
        """
        :type birthDate: str
        :type firstName: str
        :type lastName: str
        :type salutation: str
        :rtype: MeProfile
        """

        return MeProfile(
            birthDate=birthDate,
            firstName=firstName,
            lastName=lastName,
            salutation=salutation,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'MeProfile'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'birthDate'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.birthDate = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'firstName'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.firstName = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'lastName'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.lastName = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'salutation'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.salutation = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
