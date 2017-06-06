STRING = 'S'


class BaseField(object):
    value = None
    ATTRIBUTE_TYPE = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if self.ATTRIBUTE_TYPE == STRING and (isinstance(value, str) or isinstance(value, unicode)):
            self.value = value
        else:
            raise ValueError('The value \'%s\' needs to be str or unicode' % str(value))
