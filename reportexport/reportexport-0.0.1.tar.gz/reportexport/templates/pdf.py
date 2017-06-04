# -*- coding: utf-8 -*-
from cStringIO import StringIO
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from .base import Template


STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle(name='ReportDescription', fontSize=18, leftIndent=200, spaceBefore=20))


@Template.register
class PDFTemplate(Template):
    """PDF generator template."""

    extension = 'pdf'

    @staticmethod
    def render(report):
        buff = StringIO()
        doc = SimpleDocTemplate(
            buff, pagesize=letter,
            rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18,
            author='Marcello Dalponte', title='Report {}'.format(report.id)
        )

        report_type = report.type_dict

        story = []

        story.append(Paragraph('The Report', STYLES["Title"]))
        story.append(Paragraph('Organization: {}'.format(report_type['organization']), STYLES["ReportDescription"]))
        story.append(Paragraph('Reported: {}'.format(report_type['reported_at']), STYLES["ReportDescription"]))
        story.append(Paragraph('Created: {}'.format(report_type['created_at']), STYLES["ReportDescription"]))

        story.append(Spacer(1, 100))

        for item in report_type['inventory']:
            ptext = '<bullet>-</bullet>{}: {}'.format(item['name'], item['price'])
            story.append(Paragraph(ptext, STYLES["Bullet"], bulletText='-'))

        story.append(Spacer(1, 12))
        doc.build(story)

        return buff.getvalue()
