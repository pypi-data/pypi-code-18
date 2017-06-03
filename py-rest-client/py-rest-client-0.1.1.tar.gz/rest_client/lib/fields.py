class FieldMixin(object):
    """
    Mixin class for Field.
    """

    def generate_representation(self, field_name, index_number=None):
        """
        Generates name for __repr__ method.
        """
        representation = \
            "{endpoint_name}.{field_name}".\
                format(endpoint_name=self.endpoint_name, field_name=field_name)

        if index_number is not None:
            representation = "{representation}[{index_number}]".\
                format(representation=representation, index_number=index_number)

        return representation


class Field(FieldMixin):
    """
    This is place where we convert dictionaries, lists and pure variables to class fields.
    """
    def __init__(self, endpoint_name, values):
        self.endpoint_name = endpoint_name
        self.fields = values

    def __getattr__(self, field):
        field_name = field
        field_value = self.fields.get(field)
        representation = self.generate_representation(field_name)

        if isinstance(field_value, list):
            """Change list items to Field instances."""
            fields = [Field(endpoint_name=self.generate_representation(field_name, index_number),
                            values=nested_values) for index_number, nested_values in enumerate(field_value)]
            return Field(endpoint_name=representation, values=fields)

        return Field(endpoint_name=representation, values=field_value)

    def __getitem__(self, item):
        """
        When current field is a part of dictionary.
        """
        return self.fields[item]

    def __dict__(self):
        return self.fields

    def __repr__(self):
        endpoint_name = "{endpoint_name}: ".format(endpoint_name=self.endpoint_name)
        values = str(self.values()).replace(endpoint_name, '')

        return "{endpoint_name}: {values}".format(
            endpoint_name=self.endpoint_name,
            values=str(values)
        )

    def values(self):
        """
        Returns objects as dictionary.
        """
        return self.__dict__()
