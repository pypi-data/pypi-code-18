from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .constants import URL_NAME
from .forms import EmailForm
from .views_mixin import ResponseClassFallbackMixin


class EmailFormView(ResponseClassFallbackMixin, FormView):
    template_fallback = """
    <form method="post">
      {% csrf_token %}
      {{ form }}
      <input type="submit" value="Submit" />
    </form>
    """
    template_url_key_name = 'form'
    form_class = EmailForm
    success_url = None

    def get_success_url(self):
        if not self.success_url:
            self.success_url = reverse_lazy(URL_NAME['success'])

        return FormView.get_success_url(self)

    def get_initial(self):
        initial = FormView.get_initial(self)
        for key, value in self.request.GET.items():
            initial[key] = value
        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EmailFormSuccessView(ResponseClassFallbackMixin, TemplateView):
    template_fallback = """
    Form submission succes!
    """
    template_url_key_name = 'success'
