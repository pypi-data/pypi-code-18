import functools
import json
import logging

from py_zipkin.thrift import zipkin_core
from thriftpy.protocol.binary import TBinaryProtocol
from thriftpy.transport import TMemoryBuffer
from py_zipkin.zipkin import zipkin_span, ZipkinAttrs


class Service(object):
    _service_name = ""

    @classmethod
    def get_service_name(cls):
        return cls._service_name

    @classmethod
    def set_service_name(cls, service_name):
        cls._service_name = service_name


def init_service(service_name):
    Service.set_service_name(service_name)

def transport_handler(message):
    transportIn = TMemoryBuffer(message)
    protocolIn = TBinaryProtocol(transportIn)
    span = zipkin_core.Span()
    span.read(protocolIn)
    logging.info("zipkin message %s end", json.dumps(span, default=lambda x: x.__dict__))


def zipkin_handler():
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, zipkin_hander_method(getattr(cls, attr)))
        return cls

    return decorate


def zipkin_hander_method(func):
    @functools.wraps(func)
    def wapper(handler, *args, **kw):
        headers = handler.request.headers
        zipkin_attrs = ZipkinAttrs(
            trace_id=headers.get('X-B3-TraceID', None),
            span_id=headers.get('X-B3-SpanID', None),
            parent_span_id=headers.get('X-B3-ParentSpanID', None),
            flags=headers.get('X-B3-Flags', None),
            is_sampled=headers.get('X-B3-Sampled', None),
        )
        with zipkin_span(
                service_name=Service.get_service_name(),
                zipkin_attrs=zipkin_attrs if zipkin_attrs[0] else None,
                span_name=handler.__class__.__name__ + "." + func.__name__,
                transport_handler=transport_handler,
                port=6000,
                sample_rate=100,  # 0.05, # Value between 0.0 and 100.0
        ) as zipkin_context:
            result = func(handler, *args, **kw)
            zipkin_context.update_binary_annotations({'status_code': handler.get_status()})
        return result

    return wapper


def zipkin_common_method(func):
    @functools.wraps(func)
    def wapper(*args, **kw):
        with zipkin_span(
                service_name=Service.get_service_name(),
                span_name=func.__name__,
        ):
            return func(*args, **kw)
    return wapper
