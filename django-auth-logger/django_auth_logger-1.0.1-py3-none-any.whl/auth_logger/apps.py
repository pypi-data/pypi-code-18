from django.apps import AppConfig


class AuthLoggerConfig(AppConfig):
    name = 'auth_logger'

    def ready(self):
        import auth_logger.signals.handlers #noqa
