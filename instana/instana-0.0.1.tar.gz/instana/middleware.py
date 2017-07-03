import opentracing
import instana.tracer


class InstanaMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        opentracing.global_tracer = instana.tracer.InstanaTracer()
        self

    def __call__(self, request):
        span = opentracing.global_tracer.start_span("django")
        response = self.get_response(request)
        span.finish()
        return response
