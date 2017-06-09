import os
import functools
import tornado.gen
import upfluence.error_logger
import thrift.Thrift

unit_name = os.environ.get('UNIT_NAME', 'unknown')


def catcher(error_class, *err_args, **err_kwargs):
    def catcher_decorator(func):
        @functools.wraps(func)
        @tornado.gen.coroutine
        def func_wrapper(*args, **kwargs):
            try:
                result = yield tornado.gen.maybe_future(func(*args, **kwargs))
            except Exception as e:
                try:
                    class_name = args[0].__class__.__name__
                except:
                    class_name = ''

                for namespace in err_kwargs.get('exception_namespaces', []):
                    if e.__class__.__module__.startswith(namespace):
                        raise e

                upfluence.error_logger.client.capture_exception(extra={
                    'class_name': class_name,
                    'func_name': func.__name__})

                raise error_class(*err_args)

            raise tornado.gen.Return(result)

        return func_wrapper
    return catcher_decorator


default_catcher = catcher(
    thrift.Thrift.TApplicationException,
    thrift.Thrift.TApplicationException.INTERNAL_ERROR,
    exception_namespaces=['thrift'])
