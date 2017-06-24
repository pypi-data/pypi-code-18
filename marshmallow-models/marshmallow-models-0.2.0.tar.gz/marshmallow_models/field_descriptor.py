# noinspection PyProtectedMember
class FieldDescriptor(object):
    def __init__(self, field_name):
        self.field_name = field_name

    @staticmethod
    def _get_class_field(model_class, field_name):
        try:
            return model_class._schema_class._declared_fields[field_name]
        except KeyError:
            # convert KeyError into a more meaningful AttributeError
            raise AttributeError("type object '%s' has no attribute '%s'"
                                 % (model_class.__name__, field_name))

    @staticmethod
    def _get_instance_field(model_instance, field_name):
        return model_instance._schema.declared_fields[field_name]

    @staticmethod
    def _get_serialized_value(model_instance, field_name):
        try:
            return model_instance._serialized[field_name]
        except KeyError:
            # convert KeyError into a more meaningful AttributeError
            raise AttributeError("'%s' object has no attribute '%s'"
                                 % (model_instance.__class__.__name__, field_name))

    @staticmethod
    def _set_value(model_instance, field_name, value):
        pass

    @staticmethod
    def _set_serialized_value(model_instance, field_name, value):
        model_instance._serialized[field_name] = value

    def __get__(self, model_instance, model_class):
        """ Equivalent to serialization. """
        """
        (But missing and default should be the same?)
        No... constructor and setters are deserialization...
        constructor with insufficient input could use missing values...
        getting something that wasn't set would use default values...
        but yes, they should be the same...
        probably want to warn about that...
        BUT... no need to check if field is missing because it should've already been set
        ... in theory someone could load data, then delete something, then retrieve different data...
        but that seems crazy
        """

        if model_instance is None:
            # simulate that the Field is an attribute of the Model
            return self._get_class_field(model_class, self.field_name)
        else:
            # insertion of missing/default values is handled in the Model constructor
            # and by FieldDescriptor.__delete__
            return self._get_serialized_value(model_instance, self.field_name)

    def __set__(self, model_instance, value):
        """ Equivalent to deserialization. """

        field = self._get_instance_field(model_instance, self.field_name)
        # TODO convert differently
        value = field.pre_setattr(value)
        model_instance._serialized.converted[self.field_name] = value

    def __delete__(self, model_instance):
        """ Deletes the value. Should restore default or missing. """

        del model_instance._serialized[self.field_name]

        field = self._get_instance_field(model_instance, self.field_name)

        default_value = field.serialize('temp', {})

        model_instance._serialized[self.field_name] = default_value
