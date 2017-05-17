# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import io

from six.moves.urllib.parse import quote

from django.views import generic
from django.http.response import HttpResponse

from .datas import CsvDataMixin, ZipDataMixin

FormMixin = generic.edit.FormMixin


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

    def get_content_type(self):
        return self.content_type

    def get_filename(self):
        return self.download_filename

    def download(self, *args, **kwargs):
        buf = io.BytesIO()
        self.write_data(buf)
        buf.seek(0)
        response = HttpResponse(
            buf, content_type=self.get_content_type())
        response['Content-Disposition'] = (
            "attachment; filename*=utf-8'jp'{}".format(
                quote(self.get_filename().encode('UTF-8'))))
        return response


class DownloadCsvMixin(CsvDataMixin, DownloadMixin):
    def get_content_type(self):
        return 'text/csv; charset={}'.format(self.get_encoding())


class DownloadZipMixin(ZipDataMixin, DownloadMixin):
    pass
