"""
Auto-generated class for EmailDetails
"""
from .EmailDetailsTypes import EmailDetailsTypes

from . import client_support


class EmailDetails(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(email, type, verified, id=None):
        """
        :type email: str
        :type id: str
        :type type: EmailDetailsTypes
        :type verified: bool
        :rtype: EmailDetails
        """

        return EmailDetails(
            email=email,
            id=id,
            type=type,
            verified=verified,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'EmailDetails'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'email'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.email = client_support.val_factory(val, datatypes)
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

        property_name = 'type'
        val = data.get(property_name)
        if val is not None:
            datatypes = [EmailDetailsTypes]
            try:
                self.type = client_support.val_factory(val, datatypes)
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
