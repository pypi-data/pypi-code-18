import importlib

import tblib


def serialize_exception(exc):
    traceback = None
    if exc.__traceback__:
        traceback = tblib.Traceback(exc.__traceback__).to_dict()

    return (
        exc.__class__.__module__,
        exc.__class__.__name__,
        exc.args,
        traceback,
    )


def deserialize_exception(module_name, class_name, args, traceback_dict):
    try:
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
    except (ImportError, AttributeError):
        cls = type(class_name, (BaseException,), {})
        cls.__module__ = module_name

    exc = cls(*args)
    if traceback_dict is not None:
        traceback = tblib.Traceback.from_dict(traceback_dict)
        exc = exc.with_traceback(traceback.as_traceback())

    return exc
