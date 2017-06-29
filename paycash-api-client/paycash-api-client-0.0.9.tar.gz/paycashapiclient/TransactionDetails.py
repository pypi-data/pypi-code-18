"""
Auto-generated class for TransactionDetails
"""
from .Debit import Debit
from .TransactionReasons import TransactionReasons
from .TransactionStatuses import TransactionStatuses

from . import client_support


class TransactionDetails(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(**kwargs):
        """
        :type amount: float
        :type createdAt: str
        :type currency: str
        :type debit: Debit
        :type from: str
        :type fund: str
        :type memo: str
        :type merchantCode: str
        :type merchantDetails: str
        :type reason: TransactionReasons
        :type reference: str
        :type status: TransactionStatuses
        :type to: str
        :type type: str
        :type uuid: str
        :type version: float
        :rtype: TransactionDetails
        """

        return TransactionDetails(**kwargs)

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'TransactionDetails'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'amount'
        val = data.get(property_name)
        if val is not None:
            datatypes = [float]
            try:
                self.amount = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'createdAt'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.createdAt = client_support.val_factory(val, datatypes)
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

        property_name = 'debit'
        val = data.get(property_name)
        if val is not None:
            datatypes = [Debit]
            try:
                self.debit = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'from'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                setattr(self, 'from', client_support.val_factory(val, datatypes))
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'fund'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.fund = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'memo'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.memo = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'merchantCode'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.merchantCode = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'merchantDetails'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.merchantDetails = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'reason'
        val = data.get(property_name)
        if val is not None:
            datatypes = [TransactionReasons]
            try:
                self.reason = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'reference'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.reference = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'status'
        val = data.get(property_name)
        if val is not None:
            datatypes = [TransactionStatuses]
            try:
                self.status = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'to'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.to = client_support.val_factory(val, datatypes)
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

        property_name = 'uuid'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.uuid = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'version'
        val = data.get(property_name)
        if val is not None:
            datatypes = [float]
            try:
                self.version = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
