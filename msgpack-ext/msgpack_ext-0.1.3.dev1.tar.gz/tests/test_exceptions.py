from msgpack_ext import exceptions


traceback_dict = {
    'tb_frame': {'f_globals': {'__name__': '__main__'},
                 'f_code': {'co_filename': '<input>', 'co_name': '<module>'}},
    'tb_lineno': 1,
    'tb_next': None
}


def test_deserialize_exception():
    module_name = 'builtins'
    class_name = 'ValueError'
    args = ('test',)

    exc = exceptions.deserialize_exception(
        module_name,
        class_name,
        args,
        traceback_dict
    )

    assert exc.__class__.__name__ == class_name
    assert exc.__class__.__module__ == module_name
    assert exc.args == args
    assert exc.__traceback__ is not None


def test_deserialize_exception_bogus_class():
    module_name = 'fake_module'
    class_name = 'fake_error'
    args = ('also_fake',)

    exc = exceptions.deserialize_exception(
        module_name,
        class_name,
        args,
        traceback_dict
    )

    assert exc.__class__.__name__ == class_name
    assert exc.__class__.__module__ == module_name
    assert exc.args == args
    assert exc.__traceback__ is not None


def test_serialize_exception():
    exc = None

    try:
        raise ValueError('test')
    except Exception as e:
        exc = e

    obj = exceptions.serialize_exception(exc)
    module_name, class_name, args, traceback_dict = obj

    assert module_name == exc.__class__.__module__
    assert class_name == exc.__class__.__name__
    assert args == exc.args
    assert traceback_dict is not None
