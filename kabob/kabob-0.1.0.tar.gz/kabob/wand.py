class KabobError(Exception):
    pass


def _kabob_entry(vals):
    if type(vals) in [dict, str, bytearray, bytes] or not hasattr(vals, '__iter__'):
        vals = (vals,)
    for x in vals:
        yield x


class Kabob(object):
    def __init__(self, *fns):
        self.__fns = fns

    def __step(self, step):
        def wrapper(vals):
            for fn in self.__fns:
                for x in fn(vals):
                    for y in step(x):
                        yield y
        return wrapper

    def __call__(self, vals):
        for fn in self.__fns:
            for x in fn(vals):
                yield x

    def __or__(self, receiver):
        if not isinstance(receiver, Kabob):
            if callable(receiver):
                receiver = Kabob(receiver)
            else:
                raise KabobError('right hand side must be a kabob or a function: {}'.format(receiver))

        @self.__step
        def wrapper(val):
            for y in receiver(val):
                yield y
        return Kabob(wrapper)

    def __getattr__(self, name):
        @self.__step
        def wrapper(val):
            yield getattr(val, name)
        return Kabob(wrapper)

    def __getitem__(self, name):
        @self.__step
        def wrapper(val):
            yield val[name]
        return Kabob(wrapper)

    def __contains__(self, *args):
        raise KabobError('don\'t use `x in _`; use `_.contains(x)` instead')

    def contains(self, *names):
        @self.__step
        def wrapper(val):
            for name in names:
                if name not in val:
                    break
            else:
                yield val
        return Kabob(wrapper)


class KabobWand(Kabob):
    def __init__(self):
        super(KabobWand, self).__init__(_kabob_entry)

    def __call__(self, *args):
        return Kabob(*args)
