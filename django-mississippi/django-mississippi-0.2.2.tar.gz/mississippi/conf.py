from django.conf import settings


class Settings(object):
    """ Safely get this app's settings from the host app's settings """

    @property
    def MISSISSIPPI_VIEW_MAP(self) -> dict:
        return getattr(settings, 'MISSISSIPPI_VIEW_MAP', {})

    @property
    def MISSISSIPPI_SITEMAP_MAX_AGE(self) -> int:
        return getattr(settings, 'MISSISSIPPI_SITEMAP_MAX_AGE', 60 * 30)


conf = Settings()
