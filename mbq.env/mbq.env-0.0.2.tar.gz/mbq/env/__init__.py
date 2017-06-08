import os

NOT_PROVIDED = object()


class EnvException(Exception):
    pass


class Env:
    def __init__(self, prefix=None):
        if prefix is None:
            self.prefix = ''
        else:
            self.prefix = prefix + '_'

    def get(self, key, default=NOT_PROVIDED, required=True,
            coerce=NOT_PROVIDED):
        # I know, I know, coerce is a built-in function but it was removed
        # in Python 3 and I bet that if I didn't write this comment,
        # the shadowing would have gone unnoticed. Deal with it.
        key = self.prefix + key

        try:
            val = os.environ[key].strip()
        except KeyError:
            if default is not NOT_PROVIDED:
                return default

            if not required:
                return None

            raise EnvException('Missing key "{}"'.format(key))

        if coerce is not NOT_PROVIDED:
            val = coerce(val)

        return val

    def get_int(self, key, default=NOT_PROVIDED, required=True):
        try:
            return self.get(key, default=default, required=required,
                            coerce=int)
        except ValueError as e:
            raise EnvException('Could not get int: {}'.format(e))

    def get_bool(self, key, default=NOT_PROVIDED, required=True):
        return self.get(key, default=default, required=required) == '1'

    def get_csv(self, key, default=NOT_PROVIDED, required=True):
        def splitter(val):
            return [s.strip() for s in val.split(',') if s.strip()]

        return self.get(key, default=default, required=required,
                        coerce=splitter)

    def get_tokens(self, key, default=NOT_PROVIDED, required=True):
        def splitter(val):
            return [s.strip() for s in val.split() if s.strip()]

        return self.get(key, default=default, required=required,
                        coerce=splitter)

    def get_key(self, guard_type, key, required=True):
        BEGIN_GUARD = '-----BEGIN {}-----'.format(guard_type)
        END_GUARD = '-----END {}-----'.format(guard_type)
        LINE_LENGTH = 64

        val = self.get(key, required=required)

        if not val:
            return val

        # ensure key begins and ends with guards
        if not val.startswith(BEGIN_GUARD) or not val.endswith(END_GUARD):
            raise EnvException('Key must have proper BEGIN and END guards')

        # if val already has newlines, we assume it's in the right format
        if '\n' in val:
            return val

        val = val[len(BEGIN_GUARD):-len(END_GUARD)]
        key_lines = [BEGIN_GUARD]

        while val:
            key_lines.append(val[:LINE_LENGTH])
            val = val[LINE_LENGTH:]

        key_lines.append(END_GUARD)

        return '\n'.join(key_lines)


_default = Env()  # no prefix for module-based use
get = _default.get
get_bool = _default.get_bool
get_csv = _default.get_csv
get_int = _default.get_int
get_key = _default.get_key
get_tokens = _default.get_tokens
