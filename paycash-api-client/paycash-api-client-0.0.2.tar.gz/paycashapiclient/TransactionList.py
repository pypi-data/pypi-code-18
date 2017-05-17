"""
Auto-generated class for TransactionList
"""
from .TransactionDetails import TransactionDetails

from . import client_support


class TransactionList(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(number, size, totalElements, totalPages, transactions):
        """
        :type number: float
        :type size: float
        :type totalElements: float
        :type totalPages: float
        :type transactions: list[TransactionDetails]
        :rtype: TransactionList
        """

        return TransactionList(
            number=number,
            size=size,
            totalElements=totalElements,
            totalPages=totalPages,
            transactions=transactions,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'TransactionList'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'number'
        val = data.get(property_name)
        if val is not None:
            datatypes = [float]
            try:
                self.number = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'size'
        val = data.get(property_name)
        if val is not None:
            datatypes = [float]
            try:
                self.size = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'totalElements'
        val = data.get(property_name)
        if val is not None:
            datatypes = [float]
            try:
                self.totalElements = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'totalPages'
        val = data.get(property_name)
        if val is not None:
            datatypes = [float]
            try:
                self.totalPages = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'transactions'
        val = data.get(property_name)
        if val is not None:
            datatypes = [TransactionDetails]
            try:
                self.transactions = client_support.list_factory(val, datatypes)
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
