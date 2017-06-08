import json

from datetime import datetime

TYPE_ATTR = '__type__'
MODULE_ATTR = '__module__'
TIMESTAMP_ATTR = '__timestamp__'


class UnserializableException(TypeError):
    def __init__(self, type_):
        super().__init__('Type is not serializable')
        self.type = type_


def _asdict(obj):
    dict_ = {
        TYPE_ATTR: type(obj).__name__,
        MODULE_ATTR: type(obj).__module__
    }
    if isinstance(obj, datetime):
        dict_[TIMESTAMP_ATTR] = obj.timestamp()
    elif hasattr(obj, '_asdict'):
        dict_.update(obj._asdict())
    else:
        raise UnserializableException(type(obj).__name__)
    return dict_


def _fromdict(dict_: dict):
    try:
        type_, module_ = dict_.pop(TYPE_ATTR), dict_.pop(MODULE_ATTR)
    except KeyError:
        return dict_
    if type_ == datetime.__name__:
        return datetime.fromtimestamp(dict_[TIMESTAMP_ATTR])
    return Serializable.create(module_, type_, dict_)


class Serializable:
    _type_cache = {}

    def __init_subclass__(cls):
        Serializable._type_cache[(cls.__module__, cls.__name__)] = cls

    @staticmethod
    def create(module_name, type_name, dict_):
        try:
            type_ = Serializable._type_cache[(module_name, type_name)]
        except KeyError:
            type_ = type(type_name, (Serializable,), {MODULE_ATTR: module_name,
                                                      '__init__': lambda self, **kwargs: setattr(self, '__dict__',
                                                                                                 kwargs)})
        return type_(**dict_)

    def _asdict(self):
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def encode(self):
        return dumps(self)

    @staticmethod
    def decode(data):
        return loads(data)

_encoder = json.JSONEncoder(default=_asdict)
_decoder = json.JSONDecoder(object_hook=_fromdict)

dumps = _encoder.encode
loads = _decoder.decode

register_args = (dumps, loads, 'application/json', 'utf-8')
