from django.http import JsonResponse
from django.http.response import HttpResponseBase
from django.utils.cache import cc_delim_re, patch_vary_headers

from rest_framework.response import Response
from rest_framework.views import APIView

class MockableView(APIView):
    """
    This is the class which will allow you to build Mockable APIs
    """

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            # In case the API is being mocked, send the mock response
            if str(request.META.get('HTTP_MOCKABLE', "")).lower() == 'true':
                response = Response(self.mock_response, status=200, content_type="application/json")
            else:
                response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response