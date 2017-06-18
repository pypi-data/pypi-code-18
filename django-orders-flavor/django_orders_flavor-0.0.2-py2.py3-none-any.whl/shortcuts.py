from django.conf import settings
from django.urls import reverse


def paypal_context(order, request):
    assert hasattr(settings, 'PAYPAL_BUSINESS'), (
        'Missing "PAYPAL_BUSINESS" settings var'
    )

    _uri = request.build_absolute_uri

    return {
        'business': settings.PAYPAL_BUSINESS,
        'invoice': order.id.hex,
        'notify_url': _uri(reverse('paypal-ipn')),
        'return_url': _uri('paypal-success'),
        'cancel_return': _uri('paypal-cancel'),
        'currency_code': order.currency.code,
        'custom': order.id.hex
    }
