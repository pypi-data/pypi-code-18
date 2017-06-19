from nameko.rpc import MethodProxy, RpcReply
from py_zipkin import zipkin


class TracedRpcReply(RpcReply):
    def __init__(self, reply_event, zipkin_span):
        super().__init__(reply_event)
        self.zipkin_span = zipkin_span

    def result(self):
        try:
            return super().result()
        finally:
            self.zipkin_span.stop()


def patch(transport_handler):
    _call = MethodProxy._call

    def _call_traced(self: MethodProxy, *args, **kwargs):
        reply = _call(self, *args, **kwargs)
        span = zipkin.zipkin_client_span(self.service_name,
                                         self.method_name,
                                         transport_handler=transport_handler)
        span.start()
        return TracedRpcReply(reply.reply_event, span)
    MethodProxy._call = _call_traced
