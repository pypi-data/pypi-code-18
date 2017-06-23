from Products.CMFCore.Expression import Expression
from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements


class SlaveConfigValidator:
    """Validate as True when having at least one DataGrid item.
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        errors = []
        for field in value:
            for method in ('toggle_method', 'vocab_method',):
                if method in field and field[method]:
                    try:
                        expr = Expression('python: ' + field[method])
                    except Exception as e:
                        errors.append('Invalid %s "%s" for %s/%s'
                                      % (method, field[method], field['name'], field['action']))

        return True if not errors else '; '.join(errors)


isSlaveConfigValid = SlaveConfigValidator('isSlaveConfigValid')
validation.register(isSlaveConfigValid)
