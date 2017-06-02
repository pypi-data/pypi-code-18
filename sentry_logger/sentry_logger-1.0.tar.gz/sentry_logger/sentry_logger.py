from raven import Client


class SentryLogger(object):

    def __init__(self, sentry_dsn):
        self.sentry_dsn = sentry_dsn

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                sentry = Client(self.sentry_dsn)
                func_name = str(func.__name__)
                tail = str(func.__code__.co_filename)
                sentry.tags_context({
                    'function_name': func_name,
                    'related_file_name': tail
                })
                sentry.captureException()
        return wrapped_func
