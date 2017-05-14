# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

import dataproperty
from mbstrdecoder import MultiByteStrDecoder
import typepy

from .._const import FormatName
from ._text_writer import IndentationTextTableWriter


class RstTableWriter(IndentationTextTableWriter):
    """
    Base class of reStructuredText table writer.
    """

    def __init__(self):
        super(RstTableWriter, self).__init__()

        self.table_name = ""
        self.char_header_row_separator = "="
        self.char_cross_point = "+"
        self.indent_string = "    "
        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = True
        self.is_write_opening_row = True
        self.is_write_closing_row = True

        self._quote_flag_mapping = copy.deepcopy(
            dataproperty.NULL_QUOTE_FLAG_MAPPING)
        self._is_remove_line_break = True

    def write_table(self):
        self._logger.logging_write()

        self._write_line(self._get_table_directive())
        self._write_table()
        if self.is_write_null_line_after_table:
            self.write_null_line()

    def _get_table_directive(self):
        if typepy.is_null_string(self.table_name):
            return ".. table:: \n"

        return ".. table:: {}\n".format(
            MultiByteStrDecoder(self.table_name).unicode_str)

    def _write_table(self):
        self._verify_property()

        self.inc_indent_level()
        super(RstTableWriter, self)._write_table()
        self.dec_indent_level()


class RstCsvTableWriter(RstTableWriter):
    """
    A table class writer for reStructuredText
    `CSV table <http://docutils.sourceforge.net/docs/ref/rst/directives.html#id4>`__
    format.

    :Examples:

        :ref:`example-rst-csv-table-writer`
    """

    @property
    def format_name(self):
        return FormatName.RST_CSV_TABBLE

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(RstCsvTableWriter, self).__init__()

        self.column_delimiter = ", "
        self.char_cross_point = ""
        self.is_padding = False
        self.is_write_header_separator_row = False
        self.is_write_value_separator_row = False
        self.is_write_closing_row = False

        self._quote_flag_mapping[typepy.Typecode.STRING] = True

    def write_table(self):
        """
        |write_table| with reStructuredText CSV table format.

        :raises pytablewriter.EmptyTableDataError:
            If the |header_list| and the |value_matrix| is empty.

        .. note::

            - |None| values will be written as an empty string.
        """

        self._logger.logging_write()

        super(RstCsvTableWriter, self)._write_table()
        if self.is_write_null_line_after_table:
            self.write_null_line()

    def _get_opening_row_item_list(self):
        directive = ".. csv-table:: "

        if typepy.is_null_string(self.table_name):
            return [directive]

        return [directive + MultiByteStrDecoder(self.table_name).unicode_str]

    def _write_opening_row(self):
        self.dec_indent_level()
        super(RstCsvTableWriter, self)._write_opening_row()
        self.inc_indent_level()

    def _write_header(self):
        if not self.is_write_header:
            return

        if typepy.is_not_empty_sequence(self.header_list):
            self._write_line(':header: "{:s}"'.format(u'", "'.join(
                [
                    MultiByteStrDecoder(header).unicode_str
                    for header in self.header_list
                ]))
            )

        self._write_line(":widths: " + ", ".join([
            str(col_dp.ascii_char_width)
            for col_dp in self._column_dp_list
        ]))
        self._write_line()

    def _get_value_row_separator_item_list(self):
        return []

    def _get_closing_row_item_list(self):
        return []


class RstGridTableWriter(RstTableWriter):
    """
    A table writer class for reStructuredText
    `Grid Tables <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#grid-tables>`__
    format.

    :Examples:

        :ref:`example-rst-grid-table-writer`

    .. py:method:: write_table

        |write_table| with reStructuredText grid tables format.

        .. note::

            - |None| values will be written as an empty string.
    """

    @property
    def format_name(self):
        return FormatName.RST_GRID_TABBLE

    @property
    def support_split_write(self):
        return False

    def __init__(self):
        super(RstGridTableWriter, self).__init__()

        self.char_left_side_row = "|"
        self.char_right_side_row = "|"


class RstSimpleTableWriter(RstTableWriter):
    """
    A table writer class for reStructuredText
    `Simple Tables <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#simple-tables>`__
    format.

    :Examples:

        :ref:`example-rst-simple-table-writer`

    .. py:method:: write_table

        |write_table| with reStructuredText simple tables format.

        .. note::

            - |None| values will be written as an empty string.
    """

    @property
    def format_name(self):
        return FormatName.RST_SIMPLE_TABBLE

    @property
    def support_split_write(self):
        return False

    def __init__(self):
        super(RstSimpleTableWriter, self).__init__()

        self.column_delimiter = "  "
        self.char_cross_point = "  "

        self.char_opening_row = "="
        self.char_closing_row = "="

        self.is_write_value_separator_row = False
