from PIL import ImageColor


class MinValueValidator(object):

    def __init__(self, limit_value):
        self.limit_value = limit_value

    def __call__(self, value, field_name):
        if value < self.limit_value:
            raise ValueError(
                f'{field_name} must not be less {self.limit_value}'
            )


class TypeValidator(object):

    def __init__(self, required_type):
        self.required_type = required_type

    def __call__(self, value, field_name):
        if not isinstance(value, self.required_type):
            if isinstance(self.required_type, list):
                types = ", ".join([r.__name__ for r in self.required_type])
            else:
                types = self.required_type

            raise ValueError(
                f'{field_name} must be {types} type.'
            )


class ColorValidator(object):

    def __call__(self, value, field_name):
        if value:
            try:
                ImageColor.getcolor(value, 'RGB')
            except Exception as e:
                raise ValueError(f'{field_name} {e}')