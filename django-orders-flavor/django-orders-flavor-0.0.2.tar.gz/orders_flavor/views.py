from django.views.generic import DetailView
from paypal.standard.forms import PayPalPaymentsForm

from . import models
from .shortcuts import paypal_context


class PaypalOrderFormView(DetailView):
    template_name = 'orders_flavor/paypal_form.html'
    queryset = models.Order.objects.pending()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PayPalPaymentsForm(
            initial=paypal_context(
                order=self.object,
                request=self.request
            )
        )

        return context
