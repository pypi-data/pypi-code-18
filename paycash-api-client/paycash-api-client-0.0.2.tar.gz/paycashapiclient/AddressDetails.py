"""
Auto-generated class for AddressDetails
"""

from . import client_support


class AddressDetails(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(addressLine, city, country, uuid, addressLine2=None, addressLine3=None, region=None, zipCode=None):
        """
        :type addressLine: str
        :type addressLine2: str
        :type addressLine3: str
        :type city: str
        :type country: str
        :type region: str
        :type uuid: str
        :type zipCode: str
        :rtype: AddressDetails
        """

        return AddressDetails(
            addressLine=addressLine,
            addressLine2=addressLine2,
            addressLine3=addressLine3,
            city=city,
            country=country,
            region=region,
            uuid=uuid,
            zipCode=zipCode,
        )

    def __init__(self, json=None, **kwargs):
        if not json and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'AddressDetails'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'addressLine'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.addressLine = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'addressLine2'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.addressLine2 = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'addressLine3'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.addressLine3 = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

        property_name = 'city'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.city = client_support.val_factory(val, datatypes)
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

        property_name = 'region'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.region = client_support.val_factory(val, datatypes)
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

        property_name = 'zipCode'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.zipCode = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
