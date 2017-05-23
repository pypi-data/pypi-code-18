from django.apps import AppConfig

class DpuserConfig(AppConfig):
    name = 'dpuser'
    label = 'dpuser'
    verbose_name = ('dpuser')

    def ready(self):
    	import dpuser.signals.handlers
