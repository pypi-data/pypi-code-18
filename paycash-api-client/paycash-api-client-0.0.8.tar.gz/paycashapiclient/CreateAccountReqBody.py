"""
Auto-generated class for CreateAccountReqBody
"""

from . import client_support


class CreateAccountReqBody(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(currencies, type=None):
        """
        :type currencies: list[str]
        :type type: str
        :rtype: CreateAccountReqBody
        """

        return CreateAccountReqBody(
            currencies=currencies,
            type=type,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'CreateAccountReqBody'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'currencies'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.currencies = client_support.list_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'type'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.type = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
