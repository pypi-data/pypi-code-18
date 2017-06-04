# -*- coding: utf-8 -*-
"""Flask report generator."""
from __future__ import absolute_import, unicode_literals
from flask import Blueprint, abort, make_response

from .exceptions import InvalidTemplate
from .models import Report
from .templates import Template


blueprint = Blueprint('report', __name__, url_prefix='/report')


@blueprint.route('/report-<int:report_id>.<extension>')
def report_pdf(report_id, extension):
    try:
        template = Template.get_template(extension)
    except InvalidTemplate:
        abort(404, 'Report not available in "{}" format. Formats available: {}.'.format(extension, ', '.join(sorted(Template._TEMPLATES.keys()))))

    report = Report.get_by_id(report_id)

    if report is None:
        abort(404, 'Report with id "{}" does not exist.'.format(report_id))

    serialised_report = template.render(report)

    response = make_response(serialised_report)

    filename = 'report-{id}.{ext}'.format(id=report.id, ext=template.extension)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response


@blueprint.route('/healthcheck')
def healthcheck():
    return 'OK'
