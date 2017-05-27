class BaseModelMixin(object):
    def __init__(self, *args, **kwargs):
        super(BaseModelMixin, self).__init__(*args, **kwargs)
        for field in self._meta.log_fields:
            current_value = getattr(self, field, None)
            setattr(self, '__original_%s' % field, current_value)

    def has_changed(self, field_name):
        original_name = '__original_%s' % field_name
        original_value = getattr(self, original_name)
        new_value = getattr(self, field_name)

        if original_value in {None, ''} and new_value in {None, ''}:
            return False

        if original_value != new_value:
            return True

        return False

    def get_old_value(self, field_name):
        original_name = '__original_%s' % field_name
        try:
            return getattr(self, original_name)
        except AttributeError:
            raise AttributeError('`%s` is not tracked' % field_name)

    def get_new_value(self, field_name):
        return getattr(self, field_name)
