from django.conf import settings


SETTINGS = getattr(settings, "NAVBUILDER", {})
