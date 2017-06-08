# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Module `murdock.report.latex`
-----------------------------

`LaTeX`_ backend for the `.report.report` API.

.. _LaTeX: https://www.latex-project.org

.. warning::

    The formatting of the PDF results is an early work in progress.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.utils import viewitems, viewvalues

import codecs
import collections
import logging
import os
import re
import subprocess
import traceback

import murdock.report
import murdock.misc

log = logging.getLogger(__name__)

SPECIAL_CHARS = {
    r'_': r'\_', r'\\': r'\\\\', r'%': r'\%', r'&': r'\&', r'$': r'\$',
    r'#': r'\#', r'{': r'\{', r'}': r'\}', r'~': r'\~', r'^': r'\^'}

PAGEHEIGHT = 360
PAGEWIDTH = 680

class LatexError(Exception):
    pass


class Project(murdock.report.Project):
    """A class to create a Latex project.
    """

    def __init__(self, mode, title, label, outdir, user=None, build_exec=None):
        super(Project, self).__init__(
            mode=mode, title=title, label=label, outdir=outdir, user=user,
            build_exec=build_exec)

    @property
    def buildfile(self):
        """Return filepath to the builder-specific result report.
        """
        return os.path.join(self.targetdir, 'index.pdf')

    @property
    def targetdir(self):
        """Return path to builder-specific subdirectory of the build directory.
        """
        return os.path.join(self.builddir, 'pdf')

    def _new_document(self, label):
        return Document(outdir=self.outdir, label=label)

    def _write_indexfile(self):
        toc_labels = list(self._get_toc_docs())
        index = self._new_document('index')
        header = ''
        header += '\\documentclass[notitlepage,landscape,11pt]{report}\n'
        header += '\\usepackage{graphicx}\n'
        header += '\\renewcommand{\\familydefault}{\\sfdefault}\n'
        header += '\\usepackage{booktabs}\n'
        header += '\\usepackage[cm]{fullpage}\n'
        header += '\\usepackage{float}\n'
        if toc_labels:
            header += '\\makeatletter\n'
            header += '\\newcommand*{\\toccontents}{\\@starttoc{toc}}\n'
            header += '\\makeatother\n'
        if self.user is not None:
            header += '\\author{%s}\n' % self.user
        header += '\\title{%s}\n' % self.title
        header += '\\begin{document}\n'
        content = ''
        content += '\\maketitle\n'
        if toc_labels:
            content += '\\toccontents\n'
        footer = ''
        footer += '\\end{document}\n'
        index.add_paragraph(header)
        index.increase_indent()
        index.add_paragraph(content)
        if toc_labels:
            index.add_headline(0, 'Overview')
        index.add_include_directive(self.label)
        for label in toc_labels:
            index.add_include_directive(label)
        index.decrease_indent()
        index.add_paragraph(footer)
        index.write()
        return True

    def build(self):
        self._write_indexfile()
        if self.build_exec is None:
            return False
        logfilepath = os.path.join(self.outdir, 'build.log')
        log.info(
            'Build LaTeX project in `%s`.',
            murdock.misc.fmtpath(self.targetdir, self.outdir))
        rel_targetdir = os.path.relpath(self.targetdir, self.outdir)
        if not os.path.exists(self.targetdir):
            os.makedirs(self.targetdir)
        filepath = 'index.tex'
        cmd = [
            '%s' % self.build_exec, '-output-directory=%s' % rel_targetdir,
            '-interaction=nonstopmode', filepath]
        try:
            with codecs.open(logfilepath, 'w', encoding='utf-8') as f:
                for i in range(2):
                    subprocess.call(cmd, stderr=f, stdout=f, cwd=self.outdir)
        except KeyboardInterrupt:
            raise
        except:
            errmsg = traceback.format_exc().splitlines()[-1]
            log.error(
                'LaTeX project in `%s` can not be build using the executable '
                '`%s`: %s', murdock.misc.fmtpath(self.targetdir, self.outdir),
                self.build_exec, errmsg)
            return False
        return True


class Document(murdock.report.Document):

    def __init__(self, outdir, label, ext='.tex', plot_ext='.pdf'):
        super(Document, self).__init__(
            outdir=outdir, label=label, ext=ext, plot_ext=plot_ext)

    def add_figure(self, outdir, label, size, scale=None, ext=None):
        if ext is None:
            ext = self.plot_ext
        if scale is not None:
            size = (round(scale * size[0]), round(scale * size[1]))
        scale = 1
        if size[0] > PAGEWIDTH:
            scale = float(PAGEWIDTH) / size[0]
        if size[1] > PAGEWIDTH:
            scale = min(scale, float(PAGEHEIGHT) / size[1])
        width = round(scale * size[0])
        height = round(scale * size[1])
        kwargs = {'width': '%dpt' % width, 'height': '%dpt' % height}
        refpath = '%s/%s%s' % ('/'.join(outdir.split('\\')), label, ext)
        return self.fmt_figure(refpath, **kwargs)

    def add_headline(self, level, text):
        level += self.headline_offset
        text = _escape_special_chars(text)
        htypes = [
            'chapter', 'section', 'subsection', 'subsubsection', 'paragraph']
        try:
            htype = htypes[level]
        except IndexError:
            raise LatexError(
                'Headline level %d not implemented (must be <%d).' % (
                    level, len(htypes)))
        self.add_newline()
        self.add_paragraph('\\%s{%s}\n' % (htypes[level], text))
        return True

    def add_include_directive(self, label, ext=''):
        self.add_paragraph('\\include{%s%s}\n' % (label, ext))

    def fmt_bullet_list(self, struct, indent=None):
        if indent is None:
            indent = self._indent
        l = ''
        if isinstance(struct, dict):
            l += '\\begin{description}\n'
            indent += '  '
            for key, val in viewitems(struct):
                key = _escape_special_chars(key)
                if isinstance(val, list) or isinstance(val, dict):
                    l += '%s\item[%s]\n' % (indent, key)
                    l += self.fmt_bullet_list(val, indent + '  ')
                else:
                    val = _escape_special_chars(val)
                    l += '%s\item[%s] %s\n' % (indent, key, val)
            indent = indent[:-2]
            l += '\\end{description}\n'
        elif isinstance(struct, list):
            l += '%s\\begin{itemize}\n' % indent
            indent += '  '
            for val in struct:
                if isinstance(val, list) or isinstance(val, dict):
                    l += '%s\\item\n' % indent
                    l += self.fmt_bullet_list(val, indent + '  ')
                else:
                    val = _escape_special_chars(val)
                    l += '%s\\item %s\n' % (indent, val)
            indent = indent[:-2]
            l += '%s\\end{itemize}\n' % indent
        return l

    def fmt_bold(self, text):
        return r'\textbf{%s}' % text

    def fmt_figure(self, text, **kwargs):
        if kwargs:
            opt_str = ', '.join([
                '%s=%s' % (_key, _val) for _key, _val in viewitems(kwargs)])
            return r'\includegraphics[%s]{%s}' % (opt_str, text)
        else:
            return r'\includegraphics{%s}' % text

    def fmt_italic(self, text):
        return r'\textit{%s}' % text

    def get_table(self, ttype=None):
        return LatexTable(ttype=ttype, subs=self._subs)


class LatexTable(murdock.report.Table):
    """Class representing a LatexTable.
    """

    FORMATTERS = {
        None: '\\footnotesize', 'small': '\\normalsize', 'large': '\\tiny'
    }

    FONTSIZES = {
        None: 9, 'small': 11, 'large': 6
    }

    HEADERHEIGHT_CHARS = 5

    ROWSEP_CHARS, ROWSEP_REL = 1.0, 1.2

    COLSEP_CHARS, COLSEP_REL = 1, 1.6

    def __init__(self, compact=True, ttype=None, subs=None):
        super(LatexTable, self).__init__(
            compact=compact, ttype=ttype, subs=subs)
        self._col_formatters = None
        self._fontsize = self.FONTSIZES[self.ttype]
        self._formatter = self.FORMATTERS[self.ttype]
        self._header_height = self.HEADERHEIGHT_CHARS * self._fontsize
        self._col_sep = self.COLSEP_REL * self._fontsize
        self._row_sep = self.ROWSEP_CHARS * self.ROWSEP_REL * self._fontsize
        self._stable_sep = self._col_sep + self.COLSEP_CHARS * self._fontsize

    @property
    def col_formatters(self):
        if self._col_formatters is None:
            col_fmts = []
            for stable in viewvalues(self.data):
                for col in viewvalues(stable):
                    if False in (self._isnumeric(_x) for _x in col):
                        col_fmts.append('l')
                    else:
                        col_fmts.append('r')
                col_fmts.append('c')
            self._col_formatters = col_fmts[:-1]
        return self._col_formatters

    def create(self):
        t = ''
        for st in self._autosplit():
            t += st._create()
        return t

    def _approx_field_height(self, field):
        height = _parse_property(field, 'height')
        return self._fontsize if height is None else height

    def _approx_field_width(self, field):
        width = _parse_property(field, 'width')
        return self._fontsize * len(field) if width is None else width

    def _approx_height(self):
        height = 0.
        height += self._header_height
        height += (self.num_rows - 1) * self._row_sep
        height += sum(
            max(
                self._approx_field_height(_field)  for _stable in _row for
                _field in _stable
            ) for _row in self.iter_fmt_rows())
        return height

    def _approx_width(self):
        width = 0.
        width += (len(self.data) - 1) * self._stable_sep
        width += (self.num_cols - 1) * self._col_sep
        width += max(
            sum(
                self._approx_field_width(_field)  for _stable in _row for
                _field in _stable
            ) for _row in self.iter_fmt_rows())
        return width

    def _create(self):
        self._rescale_figures()
        t = '\n'
        t += '%s\n' % self.FORMATTERS[self.ttype]
        t += '\\begin{table*}[H]\n'
        t += '\\renewcommand{\\arraystretch}{%f}\n' % self.ROWSEP_REL
        t += '\\begin{tabular}{%s}\n' % ' '.join(self.col_formatters)
        t += '\\toprule\n'
        try:
            t += (' & \phantom{%s} &' % ('x' * self.COLSEP_CHARS)).join([
                '\multicolumn{%d}{c}{%s}' % (len(stable), head.strip())
                for _i, (head, stable) in enumerate(viewitems(self.data))])
            t += r'\\' + '\n'
        except AttributeError:
            pass
        i_col = 1
        for head, stable in viewitems(self.data):
            t += '\\cmidrule{%d-%d}\n' % (i_col, i_col + len(stable) - 1)
            i_col += len(stable) + 1
        t += ' && '.join(
            ' & '.join(_shead for _shead in _stable)
            for _stable in viewvalues(self.data))
        t += r'\\' + '\n'
        t += '\\midrule\n'
        for row in self.iter_fmt_rows():
            t += ' && '.join(
                ' & '.join(_field for _field in _group) for _group in row)
            t += r'\\' + '\n'
        t += '\\bottomrule\n'
        t += '\\end{tabular}\n'
        t += '\\end{table}\n'
        return t

    def _isnumeric(self, x):
        if self._subs is not None and x in self._subs:
            x = self._subs[x]
        if x.startswith('\\textbf') or x.startswith('\\textit'):
            x = x[8:-1]
        try:
            float(x)
        except ValueError:
            return False
        return True

    def _rescale_figures(self):
        factor = min(
            float(PAGEHEIGHT) / self._approx_height(),
            float(PAGEWIDTH) / self._approx_width())
        if factor >= 1:
            return True
        for prop in ('height', 'width'):
            for stable in viewvalues(self.data):
                for col in viewvalues(stable):
                    for i, field in enumerate(col):
                        val = _parse_property(field, prop)
                        if val is None:
                            continue
                        col[i] = _set_property(
                            field, prop, round(val * factor))
        return True

    def _autosplit(self):
        tables = []
        for t in self._autosplit_v():
            tables.extend(t._autosplit_h())
        return tables

    def _autosplit_h(self):
        height = self._header_height
        for i_row, row in enumerate(self.iter_fmt_rows()):
            height += max(
                self._approx_field_height(_field) for _group in row for _field
                in _group)
            if i_row > 0 and height + i_row * self._row_sep > PAGEHEIGHT:
                t1, t2 = self.split_h(i_row)
                return [t1] + t2._autosplit_h()
        return [self]

    def _autosplit_v(self):
        min_num_cols = 2 if self.num_rows > 1 else 1
        width = -self._col_sep - self._stable_sep
        for i_col, (head, stable) in enumerate(viewitems(self.data)):
            width += self._stable_sep
            for shead, col in viewitems(stable):
                width += self._col_sep
                max_field_width = max(
                    self._approx_field_width(_field) for _field in col)
                shead_width = self._fontsize * len(shead)
                width += max(max_field_width, shead_width)
                if i_col > min_num_cols and width > PAGEWIDTH:
                    t1, t2 = self.split_v(head)
                    return [t1] + t2._autosplit_v()
        return [self]


def _escape_special_chars(data):
    return murdock.report.substitute_all(data, SPECIAL_CHARS)


def _parse_property(field, prop):
    try:
        x = field.split('%s=' % prop)
        y = x[1].split('pt')
        return int(y[0])
    except IndexError:
        return None

def _set_property(field, prop, val):
    try:
        x = field.split('%s=' % prop)
        y = x[1].split('pt')
        return '%s%s=%dpt%s' % (x[0], prop, val, 'pt'.join(y[1:]))
    except IndexError:
        return None
