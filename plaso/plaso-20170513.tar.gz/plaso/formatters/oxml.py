# -*- coding: utf-8 -*-
"""The OpenXML event formatter."""

from plaso.formatters import interface
from plaso.formatters import manager


__author__ = 'David Nides (david.nides@gmail.com)'


class OpenXMLParserFormatter(interface.ConditionalEventFormatter):
  """Formatter for an OXML event."""

  DATA_TYPE = u'metadata:openxml'

  FORMAT_STRING_PIECES = [
      u'Creating App: {creating_app}',
      u'App version: {app_version}',
      u'Title: {title}',
      u'Subject: {subject}',
      u'Last saved by: {last_saved_by}',
      u'Author: {author}',
      u'Total edit time (secs): {total_edit_time}',
      u'Keywords: {keywords}',
      u'Comments: {comments}',
      u'Revision number: {revision_number}',
      u'Template: {template}',
      u'Number of pages: {number_of_pages}',
      u'Number of words: {number_of_words}',
      u'Number of characters: {number_of_characters}',
      u'Number of characters with spaces: {number_of_characters_with_spaces}',
      u'Number of lines: {number_of_lines}',
      u'Company: {company}',
      u'Manager: {manager}',
      u'Shared: {shared}',
      u'Security: {security}',
      u'Hyperlinks changed: {hyperlinks_changed}',
      u'Links up to date: {links_up_to_date}',
      u'Scale crop: {scale_crop}',
      u'Digital signature: {dig_sig}',
      u'Slides: {slides}',
      u'Hidden slides: {hidden_slides}',
      u'Presentation format: {presentation_format}',
      u'MM clips: {mm_clips}',
      u'Notes: {notes}']

  FORMAT_STRING_SHORT_PIECES = [
      u'Title: {title}',
      u'Subject: {subject}',
      u'Author: {author}']

  SOURCE_LONG = u'Open XML Metadata'
  SOURCE_SHORT = u'META'


manager.FormattersManager.RegisterFormatter(OpenXMLParserFormatter)
