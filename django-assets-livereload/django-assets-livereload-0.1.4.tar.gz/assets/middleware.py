from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from .templatetags.asset import live_reload_script


class LiveReloadMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        if not settings.DEBUG:
            raise MiddlewareNotUsed('Livereload not supported in production. Set DEBUG to False')
        super().__init__(*args, **kwargs)
        self._script = live_reload_script()

    def process_response(self, request, response):
        # Insert livereload script at the bottom of the page
        pos = response.content.find('</html>')
        response.content = response.content[:pos] + self._script + response.content[pos:]

        return response
