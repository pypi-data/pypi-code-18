# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import io

from six.moves.urllib.parse import quote

from django.http.response import HttpResponse
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView


from .datas import CsvDataMixin, ZipDataMixin


class SearchFormMixin(FormMixin):
    def get_form(self, *args, **kwargs):
        form = super(SearchFormMixin, self).get_form()
        form.bound_css_class = ''
        for i in form.fields:
            field = form.fields[i]
            field.required = False
        return form

    def get_form_kwargs(self):
        kwargs = super(SearchFormMixin, self).get_form_kwargs()
        kwargs.update({
            'data': self.request.GET,
        })
        return kwargs


class DownloadMixin(object):
    download_filename = 'download'
    content_type = 'application/octet-stream'

    def get_data_content_type(self):
        return self.content_type

    def get_filename(self):
        return self.download_filename

    def download(self, **kwargs):
        buf = io.BytesIO()
        self.write_data(buf, **kwargs)
        buf.seek(0)
        response = HttpResponse(
            buf, content_type=self.get_data_content_type())
        response['Content-Disposition'] = (
            "attachment; filename*=utf-8'jp'{}".format(
                quote(self.get_filename().encode('UTF-8'))))
        return response


class DownloadCsvMixin(CsvDataMixin, DownloadMixin):
    def get_data_content_type(self):
        return 'text/csv; charset={}'.format(self.get_encoding())


class DownloadZipMixin(ZipDataMixin, DownloadMixin):
    pass


# from https://gist.github.com/michelts/1029336
class MultipleFormsMixin(FormMixin):
    """
    A mixin that provides a way to show and handle several forms in a
    request.
    """
    form_classes = {}  # set the form classes as a mapping

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self, form_classes):
        return dict([(key, klass(**self.get_form_kwargs()))
                     for key, klass in form_classes.items()])

    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))


class ProcessMultipleFormsView(ProcessFormView):
    """
    A mixin that processes multiple forms on POST. Every form must be
    valid.
    """
    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)


class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """


class MultipleFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaing several forms, and rendering a template response.
    """
