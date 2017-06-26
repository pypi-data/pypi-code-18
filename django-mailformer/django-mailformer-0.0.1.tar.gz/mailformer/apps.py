from django.apps import AppConfig


class MailFormer(AppConfig):
    name = 'mailformer'
    verbose_name = "Django Mailformer"

    def ready(self):
        from .signals import listeners  # noqa
