from schematics.models import Model, ModelMeta
from schematics.types import ModelType


__version__ = '0.1.0'


def model(_schema_dict=None, **kwargs):
    _schema_dict = dict(_schema_dict or kwargs)  # create copy for changes

    for key, value in _schema_dict.items():
        if isinstance(value, dict):
            _schema_dict[key] = nested_model(value)

    return ModelMeta('AnonymousModel', (Model,), _schema_dict)


model_factory = model  # alternative import name


def nested(*args, **kwargs):
    return ModelType(model(*args, **kwargs))


nested_model = nested  # alternative import name
