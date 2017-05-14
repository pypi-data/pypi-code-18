# -*- coding: utf-8 -*-
"""
    sphinx.writers.latex
    ~~~~~~~~~~~~~~~~~~~~

    Custom docutils writer for LaTeX.

    Much of this code is adapted from Dave Kuhlman's "docpy" writer from his
    docutils sandbox.

    :copyright: Copyright 2007-2017 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
import sys
from os import path
import warnings

from six import itervalues, text_type
from docutils import nodes, writers
from docutils.writers.latex2e import Babel

from sphinx import addnodes
from sphinx import highlighting
from sphinx.errors import SphinxError
from sphinx.deprecation import RemovedInSphinx16Warning
from sphinx.locale import admonitionlabels, _
from sphinx.util import split_into
from sphinx.util.i18n import format_date
from sphinx.util.nodes import clean_astext, traverse_parent
from sphinx.util.template import LaTeXRenderer
from sphinx.util.texescape import tex_escape_map, tex_replace_map
from sphinx.util.smartypants import educate_quotes_latex


BEGIN_DOC = r'''
\begin{document}
%(shorthandoff)s
%(maketitle)s
%(tableofcontents)s
'''


DEFAULT_TEMPLATE = 'latex/content.tex_t'
URI_SCHEMES = ('mailto:', 'http:', 'https:', 'ftp:')
SECNUMDEPTH = 3

DEFAULT_SETTINGS = {
    'latex_engine':    'pdflatex',
    'papersize':       'letterpaper',
    'pointsize':       '10pt',
    'pxunit':          '.75bp',
    'classoptions':    '',
    'extraclassoptions': '',
    'maxlistdepth':    '',
    'sphinxpkgoptions':     '',
    'sphinxsetup':     '',
    'passoptionstopackages': '',
    'geometry':        '\\usepackage{geometry}',
    'inputenc':        '',
    'utf8extra':       '',
    'cmappkg':         '\\usepackage{cmap}',
    'fontenc':         '\\usepackage[T1]{fontenc}',
    'amsmath':         '\\usepackage{amsmath,amssymb,amstext}',
    'multilingual':    '',
    'babel':           '\\usepackage{babel}',
    'polyglossia':     '',
    'fontpkg':         '\\usepackage{times}',
    'fncychap':        '\\usepackage[Bjarne]{fncychap}',
    'longtable':       '\\usepackage{longtable}',
    'hyperref':        ('% Include hyperref last.\n'
                        '\\usepackage{hyperref}\n'
                        '% Fix anchor placement for figures with captions.\n'
                        '\\usepackage{hypcap}% it must be loaded after hyperref.\n'
                        '% Set up styles of URL: it should be placed after hyperref.\n'
                        '\\urlstyle{same}'),
    'usepackages':     '',
    'numfig_format':   '',
    'contentsname':    '',
    'preamble':        '',
    'title':           '',
    'date':            '',
    'release':         '',
    'author':          '',
    'logo':            '',
    'releasename':     '',
    'makeindex':       '\\makeindex',
    'shorthandoff':    '',
    'maketitle':       '\\maketitle',
    'tableofcontents': '\\sphinxtableofcontents',
    'atendofbody':     '',
    'printindex':      '\\printindex',
    'transition':      '\n\n\\bigskip\\hrule\\bigskip\n\n',
    'figure_align':    'htbp',
    'tocdepth':        '',
    'secnumdepth':     '',
    'pageautorefname': '',
}

ADDITIONAL_SETTINGS = {
    'pdflatex': {
        'inputenc':     '\\usepackage[utf8]{inputenc}',
        'utf8extra':   ('\\ifdefined\\DeclareUnicodeCharacter\n'
                        ' \\ifdefined\\DeclareUnicodeCharacterAsOptional\\else\n'
                        '  \\DeclareUnicodeCharacter{00A0}{\\nobreakspace}\n'
                        '\\fi\\fi'),
    },
    'xelatex': {
        'latex_engine': 'xelatex',
        'polyglossia':  '\\usepackage{polyglossia}',
        'babel':        '',
        'fontenc':      '\\usepackage{fontspec}',
        'fontpkg':      '',
        'utf8extra':   ('\\catcode`^^^^00a0\\active\\protected\\def^^^^00a0'
                        '{\\leavevmode\\nobreak\\ }'),
    },
    'lualatex': {
        'latex_engine': 'lualatex',
        'utf8extra':   ('\\catcode`^^^^00a0\\active\\protected\\def^^^^00a0'
                        '{\\leavevmode\\nobreak\\ }'),
    },
    'platex': {
        'latex_engine': 'platex',
        'geometry':     '\\usepackage[dvipdfm]{geometry}',
    },
}


class collected_footnote(nodes.footnote):
    """Footnotes that are collected are assigned this class."""


class UnsupportedError(SphinxError):
    category = 'Markup is unsupported in LaTeX'


class LaTeXWriter(writers.Writer):

    supported = ('sphinxlatex',)

    settings_spec = ('LaTeX writer options', '', (
        ('Document name', ['--docname'], {'default': ''}),
        ('Document class', ['--docclass'], {'default': 'manual'}),
        ('Author', ['--author'], {'default': ''}),
    ))
    settings_defaults = {}

    output = None

    def __init__(self, builder):
        writers.Writer.__init__(self)
        self.builder = builder
        self.translator_class = (
            self.builder.translator_class or LaTeXTranslator)

    def translate(self):
        transform = ShowUrlsTransform(self.document)
        transform.apply()
        visitor = self.translator_class(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = visitor.astext()


# Helper classes

class ExtBabel(Babel):
    def __init__(self, language_code):
        super(ExtBabel, self).__init__(language_code or '')
        self.language_code = language_code

    def get_shorthandoff(self):
        shortlang = self.language.split('_')[0]
        if shortlang in ('de', 'ngerman', 'sl', 'slovene', 'pt', 'portuges',
                         'es', 'spanish', 'nl', 'dutch', 'pl', 'polish', 'it',
                         'italian'):
            return '\\ifnum\\catcode`\\"=\\active\\shorthandoff{"}\\fi'
        elif shortlang in ('tr', 'turkish'):
            # memo: if ever Sphinx starts supporting 'Latin', do as for Turkish
            return '\\ifnum\\catcode`\\=\\string=\\active\\shorthandoff{=}\\fi'
        return ''

    def uses_cyrillic(self):
        shortlang = self.language.split('_')[0]
        return shortlang in ('bg', 'bulgarian', 'kk', 'kazakh',
                             'mn', 'mongolian', 'ru', 'russian',
                             'uk', 'ukrainian')

    def is_supported_language(self):
        return bool(super(ExtBabel, self).get_language())

    def get_language(self):
        language = super(ExtBabel, self).get_language()
        if not language:
            return 'english'  # fallback to english
        else:
            return language


class ShowUrlsTransform(object):
    expanded = False

    def __init__(self, document):
        self.document = document

    def apply(self):
        # replace id_prefix temporarily
        id_prefix = self.document.settings.id_prefix
        self.document.settings.id_prefix = 'show_urls'

        self.expand_show_urls()
        if self.expanded:
            self.renumber_footnotes()

        # restore id_prefix
        self.document.settings.id_prefix = id_prefix

    def expand_show_urls(self):
        show_urls = self.document.settings.env.config.latex_show_urls
        if show_urls is False or show_urls == 'no':
            return

        for node in self.document.traverse(nodes.reference):
            uri = node.get('refuri', '')
            if uri.startswith(URI_SCHEMES):
                if uri.startswith('mailto:'):
                    uri = uri[7:]
                if node.astext() != uri:
                    index = node.parent.index(node)
                    if show_urls == 'footnote':
                        footnote_nodes = self.create_footnote(uri)
                        for i, fn in enumerate(footnote_nodes):
                            node.parent.insert(index + i + 1, fn)

                        self.expanded = True
                    else:  # all other true values (b/w compat)
                        textnode = nodes.Text(" (%s)" % uri)
                        node.parent.insert(index + 1, textnode)

    def create_footnote(self, uri):
        label = nodes.label('', '#')
        para = nodes.paragraph()
        para.append(nodes.reference('', nodes.Text(uri), refuri=uri, nolinkurl=True))
        footnote = nodes.footnote(uri, label, para, auto=1)
        footnote['names'].append('#')
        self.document.note_autofootnote(footnote)

        label = nodes.Text('#')
        footnote_ref = nodes.footnote_reference('[#]_', label, auto=1,
                                                refid=footnote['ids'][0])
        self.document.note_autofootnote_ref(footnote_ref)
        footnote.add_backref(footnote_ref['ids'][0])

        return [footnote, footnote_ref]

    def renumber_footnotes(self):
        def is_used_number(number):
            for node in self.document.traverse(nodes.footnote):
                if not node.get('auto') and number in node['names']:
                    return True

            return False

        def is_auto_footnote(node):
            return isinstance(node, nodes.footnote) and node.get('auto')

        def footnote_ref_by(node):
            ids = node['ids']
            parent = list(traverse_parent(node, (nodes.document, addnodes.start_of_file)))[0]

            def is_footnote_ref(node):
                return (isinstance(node, nodes.footnote_reference) and
                        ids[0] == node['refid'] and
                        parent in list(traverse_parent(node)))

            return is_footnote_ref

        startnum = 1
        for footnote in self.document.traverse(is_auto_footnote):
            while True:
                label = str(startnum)
                startnum += 1
                if not is_used_number(label):
                    break

            old_label = footnote[0].astext()
            footnote.remove(footnote[0])
            footnote.insert(0, nodes.label('', label))
            if old_label in footnote['names']:
                footnote['names'].remove(old_label)
            footnote['names'].append(label)

            for footnote_ref in self.document.traverse(footnote_ref_by(footnote)):
                footnote_ref.remove(footnote_ref[0])
                footnote_ref += nodes.Text(label)


class Table(object):
    def __init__(self):
        self.col = 0
        self.colcount = 0
        self.colspec = None
        self.rowcount = 0
        self.had_head = False
        self.has_problematic = False
        self.has_verbatim = False
        self.caption = None
        self.longtable = False


def escape_abbr(text):
    """Adjust spacing after abbreviations."""
    return re.sub('\.(?=\s|$)', '.\\@', text)


def rstdim_to_latexdim(width_str):
    """Convert `width_str` with rst length to LaTeX length."""
    match = re.match('^(\d*\.?\d*)\s*(\S*)$', width_str)
    if not match:
        raise ValueError
    res = width_str
    amount, unit = match.groups()[:2]
    float(amount)  # validate amount is float
    if unit in ('', "px"):
        res = "%s\\sphinxpxdimen" % amount
    elif unit == 'pt':
        res = '%sbp' % amount  # convert to 'bp'
    elif unit == "%":
        res = "%.3f\\linewidth" % (float(amount) / 100.0)
    return res


class LaTeXTranslator(nodes.NodeVisitor):
    sectionnames = ["part", "chapter", "section", "subsection",
                    "subsubsection", "paragraph", "subparagraph"]

    ignore_missing_images = False

    # sphinx specific document classes
    docclasses = ('howto', 'manual')

    def __init__(self, document, builder):
        nodes.NodeVisitor.__init__(self, document)
        self.builder = builder
        self.body = []

        # flags
        self.in_title = 0
        self.in_production_list = 0
        self.in_footnote = 0
        self.in_caption = 0
        self.in_container_literal_block = 0
        self.in_term = 0
        self.in_merged_cell = 0
        self.in_minipage = 0
        self.first_document = 1
        self.this_is_the_title = 1
        self.literal_whitespace = 0
        self.no_contractions = 0
        self.in_parsed_literal = 0
        self.compact_list = 0
        self.first_param = 0
        self.remember_multirow = {}
        self.remember_multirowcol = {}

        # determine top section level
        if builder.config.latex_toplevel_sectioning:
            self.top_sectionlevel = \
                self.sectionnames.index(builder.config.latex_toplevel_sectioning)
        else:
            if document.settings.docclass == 'howto':
                self.top_sectionlevel = 2
            else:
                self.top_sectionlevel = 1

        # sort out some elements
        self.elements = DEFAULT_SETTINGS.copy()
        self.elements.update(ADDITIONAL_SETTINGS.get(builder.config.latex_engine, {}))
        # allow the user to override them all
        self.check_latex_elements()
        self.elements.update(builder.config.latex_elements)

        # but some have other interface in config file
        self.elements.update({
            'wrapperclass': self.format_docclass(document.settings.docclass),
            # if empty, the title is set to the first section title
            'title':        document.settings.title,    # treat as a raw LaTeX code
            'release':      self.encode(builder.config.release),
            'author':       document.settings.author,   # treat as a raw LaTeX code
            'indexname':    _('Index'),
        })
        if not self.elements['releasename']:
            self.elements.update({
                'releasename':  _('Release'),
            })
        if not builder.config.latex_keep_old_macro_names:
            self.elements['sphinxpkgoptions'] = 'dontkeepoldnames'
        if document.settings.docclass == 'howto':
            docclass = builder.config.latex_docclass.get('howto', 'article')
        else:
            docclass = builder.config.latex_docclass.get('manual', 'report')
        self.elements['docclass'] = docclass
        if builder.config.today:
            self.elements['date'] = builder.config.today
        else:
            self.elements['date'] = format_date(builder.config.today_fmt or _('%b %d, %Y'),
                                                language=builder.config.language)
        if builder.config.latex_logo:
            # no need for \\noindent here, used in flushright
            self.elements['logo'] = '\\sphinxincludegraphics{%s}\\par' % \
                                    path.basename(builder.config.latex_logo)

        if builder.config.language \
           and 'fncychap' not in builder.config.latex_elements:
            # use Sonny style if any language specified
            self.elements['fncychap'] = '\\usepackage[Sonny]{fncychap}'

        self.babel = ExtBabel(builder.config.language)
        if builder.config.language and not self.babel.is_supported_language():
            # emit warning if specified language is invalid
            # (only emitting, nothing changed to processing)
            self.builder.warn('no Babel option known for language %r' %
                              builder.config.language)

        # simply use babel.get_language() always, as get_language() returns
        # 'english' even if language is invalid or empty
        self.elements['classoptions'] += ',' + self.babel.get_language()

        # set up multilingual module...
        # 'babel' key is public and user setting must be obeyed
        if self.elements['babel']:
            # this branch is not taken for xelatex with writer default settings
            self.elements['multilingual'] = self.elements['babel']
            if builder.config.language:
                self.elements['shorthandoff'] = self.babel.get_shorthandoff()

                # Times fonts don't work with Cyrillic languages
                if self.babel.uses_cyrillic() \
                   and 'fontpkg' not in builder.config.latex_elements:
                    self.elements['fontpkg'] = ''

                # pTeX (Japanese TeX) for support
                if builder.config.language == 'ja':
                    # use dvipdfmx as default class option in Japanese
                    self.elements['classoptions'] = ',dvipdfmx'
                    # disable babel which has not publishing quality in Japanese
                    self.elements['babel'] = ''
                    self.elements['multilingual'] = ''
                    # disable fncychap in Japanese documents
                    self.elements['fncychap'] = ''
        elif self.elements['polyglossia']:
            self.elements['multilingual'] = '%s\n\\setmainlanguage{%s}' % \
                (self.elements['polyglossia'], self.babel.get_language())

        if getattr(builder, 'usepackages', None):
            def declare_package(packagename, options=None):
                if options:
                    return '\\usepackage[%s]{%s}' % (options, packagename)
                else:
                    return '\\usepackage{%s}' % (packagename,)
            usepackages = (declare_package(*p) for p in builder.usepackages)
            self.elements['usepackages'] += "\n".join(usepackages)
        if document.get('tocdepth'):
            # redece tocdepth if `part` or `chapter` is used for top_sectionlevel
            #   tocdepth = -1: show only parts
            #   tocdepth =  0: show parts and chapters
            #   tocdepth =  1: show parts, chapters and sections
            #   tocdepth =  2: show parts, chapters, sections and subsections
            #   ...
            tocdepth = document['tocdepth'] + self.top_sectionlevel - 2
            maxdepth = len(self.sectionnames) - self.top_sectionlevel
            if tocdepth > maxdepth:
                self.builder.warn('too large :maxdepth:, ignored.')
                tocdepth = maxdepth

            self.elements['tocdepth'] = '\\setcounter{tocdepth}{%d}' % tocdepth
            if tocdepth >= SECNUMDEPTH:
                # Increase secnumdepth if tocdepth is depther than default SECNUMDEPTH
                self.elements['secnumdepth'] = '\\setcounter{secnumdepth}{%d}' % tocdepth

        if getattr(document.settings, 'contentsname', None):
            self.elements['contentsname'] = \
                self.babel_renewcommand('\\contentsname', document.settings.contentsname)

        if self.elements['maxlistdepth']:
            self.elements['sphinxpkgoptions'] += (',maxlistdepth=%s' %
                                                  self.elements['maxlistdepth'])
        if self.elements['sphinxpkgoptions']:
            self.elements['sphinxpkgoptions'] = ('[%s]' %
                                                 self.elements['sphinxpkgoptions'])
        if self.elements['sphinxsetup']:
            self.elements['sphinxsetup'] = ('\\sphinxsetup{%s}' %
                                            self.elements['sphinxsetup'])
        if self.elements['extraclassoptions']:
            self.elements['classoptions'] += ',' + \
                                             self.elements['extraclassoptions']
        self.elements['pageautorefname'] = \
            self.babel_defmacro('\\pageautorefname', self.encode(_('page')))
        self.elements['numfig_format'] = self.generate_numfig_format(builder)

        self.highlighter = highlighting.PygmentsBridge(
            'latex',
            builder.config.pygments_style, builder.config.trim_doctest_flags)
        self.context = []
        self.descstack = []
        self.bibitems = []
        self.table = None
        self.next_table_colspec = None
        # stack of [language, linenothreshold] settings per file
        # the first item here is the default and must not be changed
        # the second item is the default for the master file and can be changed
        # by .. highlight:: directive in the master file
        self.hlsettingstack = 2 * [[builder.config.highlight_language,
                                    sys.maxsize]]
        self.bodystack = []
        self.footnotestack = []
        self.footnote_restricted = False
        self.pending_footnotes = []
        self.curfilestack = []
        self.handled_abbrs = set()
        self.next_hyperlink_ids = {}
        self.next_section_ids = set()

    def pushbody(self, newbody):
        self.bodystack.append(self.body)
        self.body = newbody

    def popbody(self):
        body = self.body
        self.body = self.bodystack.pop()
        return body

    def push_hyperlink_ids(self, figtype, ids):
        hyperlink_ids = self.next_hyperlink_ids.setdefault(figtype, set())
        hyperlink_ids.update(ids)

    def pop_hyperlink_ids(self, figtype):
        return self.next_hyperlink_ids.pop(figtype, set())

    def check_latex_elements(self):
        for key in self.builder.config.latex_elements:
            if key not in self.elements:
                msg = _("Unknown configure key: latex_elements[%r] is ignored.")
                self.builder.warn(msg % key)

    def restrict_footnote(self, node):
        if self.footnote_restricted is False:
            self.footnote_restricted = node
            self.pending_footnotes = []

    def unrestrict_footnote(self, node):
        if self.footnote_restricted == node:
            self.footnote_restricted = False
            for footnode in self.pending_footnotes:
                footnode['footnotetext'] = True
                footnode.walkabout(self)
            self.pending_footnotes = []

    def format_docclass(self, docclass):
        """ prepends prefix to sphinx document classes
        """
        if docclass in self.docclasses:
            docclass = 'sphinx' + docclass
        return docclass

    def astext(self):
        self.elements.update({
            'body': u''.join(self.body),
            'indices': self.generate_indices()
        })

        template_path = path.join(self.builder.srcdir, '_templates', 'latex.tex_t')
        if path.exists(template_path):
            return LaTeXRenderer().render(template_path, self.elements)
        else:
            return LaTeXRenderer().render(DEFAULT_TEMPLATE, self.elements)

    def hypertarget(self, id, withdoc=True, anchor=True):
        if withdoc:
            id = self.curfilestack[-1] + ':' + id
        return (anchor and '\\phantomsection' or '') + \
            '\\label{%s}' % self.idescape(id)

    def hyperlink(self, id):
        return '{\\hyperref[%s]{' % self.idescape(id)

    def hyperpageref(self, id):
        return '\\autopageref*{%s}' % self.idescape(id)

    def idescape(self, id):
        return '\\detokenize{%s}' % text_type(id).translate(tex_replace_map).\
            encode('ascii', 'backslashreplace').decode('ascii').\
            replace('\\', '_')

    def babel_renewcommand(self, command, definition):
        if self.elements['multilingual']:
            prefix = '\\addto\\captions%s{' % self.babel.get_language()
            suffix = '}'
        else:  # babel is disabled (mainly for Japanese environment)
            prefix = ''
            suffix = ''

        return ('%s\\renewcommand{%s}{%s}%s\n' % (prefix, command, definition, suffix))

    def babel_defmacro(self, name, definition):
        if self.elements['babel']:
            prefix = '\\addto\\extras%s{' % self.babel.get_language()
            suffix = '}'
        else:  # babel is disabled (mainly for Japanese environment)
            prefix = ''
            suffix = ''

        return ('%s\\def%s{%s}%s\n' % (prefix, name, definition, suffix))

    def generate_numfig_format(self, builder):
        ret = []
        figure = self.builder.config.numfig_format['figure'].split('%s', 1)
        if len(figure) == 1:
            ret.append('\\def\\fnum@figure{%s}\n' %
                       text_type(figure[0]).strip().translate(tex_escape_map))
        else:
            definition = text_type(figure[0]).strip().translate(tex_escape_map)
            ret.append(self.babel_renewcommand('\\figurename', definition))
            if figure[1]:
                ret.append('\\makeatletter\n')
                ret.append('\\def\\fnum@figure{\\figurename\\thefigure%s}\n' %
                           text_type(figure[1]).strip().translate(tex_escape_map))
                ret.append('\\makeatother\n')

        table = self.builder.config.numfig_format['table'].split('%s', 1)
        if len(table) == 1:
            ret.append('\\def\\fnum@table{%s}\n' %
                       text_type(table[0]).strip().translate(tex_escape_map))
        else:
            definition = text_type(table[0]).strip().translate(tex_escape_map)
            ret.append(self.babel_renewcommand('\\tablename', definition))
            if table[1]:
                ret.append('\\makeatletter\n')
                ret.append('\\def\\fnum@table{\\tablename\\thetable%s}\n' %
                           text_type(table[1]).strip().translate(tex_escape_map))
                ret.append('\\makeatother\n')

        codeblock = self.builder.config.numfig_format['code-block'].split('%s', 1)
        if len(codeblock) == 1:
            pass  # FIXME
        else:
            definition = text_type(codeblock[0]).strip().translate(tex_escape_map)
            ret.append(self.babel_renewcommand('\\literalblockname', definition))
            if codeblock[1]:
                pass  # FIXME

        return ''.join(ret)

    def generate_indices(self):
        def generate(content, collapsed):
            ret.append('\\begin{sphinxtheindex}\n')
            ret.append('\\def\\bigletter#1{{\\Large\\sffamily#1}'
                       '\\nopagebreak\\vspace{1mm}}\n')
            for i, (letter, entries) in enumerate(content):
                if i > 0:
                    ret.append('\\indexspace\n')
                ret.append('\\bigletter{%s}\n' %
                           text_type(letter).translate(tex_escape_map))
                for entry in entries:
                    if not entry[3]:
                        continue
                    ret.append('\\item {\\sphinxstyleindexentry{%s}}' % self.encode(entry[0]))
                    if entry[4]:
                        # add "extra" info
                        ret.append('\\sphinxstyleindexextra{%s}' % self.encode(entry[4]))
                    ret.append('\\sphinxstyleindexpageref{%s:%s}\n' %
                               (entry[2], self.idescape(entry[3])))
            ret.append('\\end{sphinxtheindex}\n')

        ret = []
        # latex_domain_indices can be False/True or a list of index names
        indices_config = self.builder.config.latex_domain_indices
        if indices_config:
            for domain in itervalues(self.builder.env.domains):
                for indexcls in domain.indices:
                    indexname = '%s-%s' % (domain.name, indexcls.name)
                    if isinstance(indices_config, list):
                        if indexname not in indices_config:
                            continue
                    # deprecated config value
                    if indexname == 'py-modindex' and \
                       not self.builder.config.latex_use_modindex:
                        continue
                    content, collapsed = indexcls(domain).generate(
                        self.builder.docnames)
                    if not content:
                        continue
                    ret.append(u'\\renewcommand{\\indexname}{%s}\n' %
                               indexcls.localname)
                    generate(content, collapsed)

        return ''.join(ret)

    def visit_document(self, node):
        self.footnotestack.append(self.collect_footnotes(node))
        self.curfilestack.append(node.get('docname', ''))
        if self.first_document == 1:
            # the first document is all the regular content ...
            self.body.append(BEGIN_DOC % self.elements)
            self.first_document = 0
        elif self.first_document == 0:
            # ... and all others are the appendices
            self.body.append(u'\n\\appendix\n')
            self.first_document = -1
        if 'docname' in node:
            self.body.append(self.hypertarget(':doc'))
        # "- 1" because the level is increased before the title is visited
        self.sectionlevel = self.top_sectionlevel - 1

    def depart_document(self, node):
        if self.bibitems:
            widest_label = ""
            for bi in self.bibitems:
                if len(widest_label) < len(bi[0]):
                    widest_label = bi[0]
            self.body.append(u'\n\\begin{sphinxthebibliography}{%s}\n' % widest_label)
            for bi in self.bibitems:
                target = self.hypertarget(bi[2] + ':' + bi[3],
                                          withdoc=False)
                self.body.append(u'\\bibitem[%s]{%s}{%s %s}\n' %
                                 (self.encode(bi[0]), self.idescape(bi[0]),
                                  target, bi[1]))
            self.body.append(u'\\end{sphinxthebibliography}\n')
            self.bibitems = []

    def visit_start_of_file(self, node):
        # collect new footnotes
        self.footnotestack.append(self.collect_footnotes(node))
        # also add a document target
        self.next_section_ids.add(':doc')
        self.curfilestack.append(node['docname'])
        # use default highlight settings for new file
        self.hlsettingstack.append(self.hlsettingstack[0])

    def collect_footnotes(self, node):
        def footnotes_under(n):
            if isinstance(n, nodes.footnote):
                yield n
            else:
                for c in n.children:
                    if isinstance(c, addnodes.start_of_file):
                        continue
                    for k in footnotes_under(c):
                        yield k
        fnotes = {}
        for fn in footnotes_under(node):
            num = fn.children[0].astext().strip()
            newnode = collected_footnote(*fn.children, number=num)
            fnotes[num] = [newnode, False]
        return fnotes

    def depart_start_of_file(self, node):
        self.footnotestack.pop()
        self.curfilestack.pop()
        self.hlsettingstack.pop()

    def visit_highlightlang(self, node):
        self.hlsettingstack[-1] = [node['lang'], node['linenothreshold']]
        raise nodes.SkipNode

    def visit_section(self, node):
        if not self.this_is_the_title:
            self.sectionlevel += 1
        self.body.append('\n\n')
        if node.get('ids'):
            self.next_section_ids.update(node['ids'])

    def depart_section(self, node):
        self.sectionlevel = max(self.sectionlevel - 1,
                                self.top_sectionlevel - 1)

    def visit_problematic(self, node):
        self.body.append(r'{\color{red}\bfseries{}')

    def depart_problematic(self, node):
        self.body.append('}')

    def visit_topic(self, node):
        self.in_minipage = 1
        self.body.append('\n\\begin{sphinxShadowBox}\n')

    def depart_topic(self, node):
        self.in_minipage = 0
        self.body.append('\\end{sphinxShadowBox}\n')
    visit_sidebar = visit_topic
    depart_sidebar = depart_topic

    def visit_glossary(self, node):
        pass

    def depart_glossary(self, node):
        pass

    def visit_productionlist(self, node):
        self.body.append('\n\n\\begin{productionlist}\n')
        self.in_production_list = 1

    def depart_productionlist(self, node):
        self.body.append('\\end{productionlist}\n\n')
        self.in_production_list = 0

    def visit_production(self, node):
        if node['tokenname']:
            tn = node['tokenname']
            self.body.append(self.hypertarget('grammar-token-' + tn))
            self.body.append('\\production{%s}{' % self.encode(tn))
        else:
            self.body.append('\\productioncont{')

    def depart_production(self, node):
        self.body.append('}\n')

    def visit_transition(self, node):
        self.body.append(self.elements['transition'])

    def depart_transition(self, node):
        pass

    def visit_title(self, node):
        parent = node.parent
        if isinstance(parent, addnodes.seealso):
            # the environment already handles this
            raise nodes.SkipNode
        elif isinstance(parent, nodes.section):
            if self.this_is_the_title:
                if len(node.children) != 1 and not isinstance(node.children[0],
                                                              nodes.Text):
                    self.builder.warn('document title is not a single Text node',
                                      (self.curfilestack[-1], node.line))
                if not self.elements['title']:
                    # text needs to be escaped since it is inserted into
                    # the output literally
                    self.elements['title'] = node.astext().translate(tex_escape_map)
                self.this_is_the_title = 0
                raise nodes.SkipNode
            else:
                short = ''
                if node.traverse(nodes.image):
                    short = ('[%s]' %
                             u' '.join(clean_astext(node).split()).translate(tex_escape_map))

                try:
                    self.body.append(r'\%s%s{' % (self.sectionnames[self.sectionlevel], short))
                except IndexError:
                    # just use "subparagraph", it's not numbered anyway
                    self.body.append(r'\%s%s{' % (self.sectionnames[-1], short))
                self.context.append('}\n')

                self.restrict_footnote(node)
                if self.next_section_ids:
                    for id in self.next_section_ids:
                        self.context[-1] += self.hypertarget(id, anchor=False)
                    self.next_section_ids.clear()
        elif isinstance(parent, nodes.topic):
            self.body.append(r'\sphinxstyletopictitle{')
            self.context.append('}\n')
        elif isinstance(parent, nodes.sidebar):
            self.body.append(r'\sphinxstylesidebartitle{')
            self.context.append('}\n')
        elif isinstance(parent, nodes.Admonition):
            self.body.append('{')
            self.context.append('}\n')
        elif isinstance(parent, nodes.table):
            # Redirect body output until title is finished.
            self.pushbody([])
        else:
            self.builder.warn(
                'encountered title node not in section, topic, table, '
                'admonition or sidebar',
                (self.curfilestack[-1], node.line or ''))
            self.body.append('\\sphinxstyleothertitle{')
            self.context.append('}\n')
        self.in_title = 1

    def depart_title(self, node):
        self.in_title = 0
        if isinstance(node.parent, nodes.table):
            self.table.caption = self.popbody()
        else:
            self.body.append(self.context.pop())
        self.unrestrict_footnote(node)

    def visit_subtitle(self, node):
        if isinstance(node.parent, nodes.sidebar):
            self.body.append('\\sphinxstylesidebarsubtitle{')
            self.context.append('}\n')
        else:
            self.context.append('')

    def depart_subtitle(self, node):
        self.body.append(self.context.pop())

    def visit_desc(self, node):
        self.body.append('\n\n\\begin{fulllineitems}\n')
        if self.table:
            self.table.has_problematic = True

    def depart_desc(self, node):
        self.body.append('\n\\end{fulllineitems}\n\n')

    def _visit_signature_line(self, node):
        for child in node:
            if isinstance(child, addnodes.desc_parameterlist):
                self.body.append(r'\pysiglinewithargsret{')
                break
        else:
            self.body.append(r'\pysigline{')

    def _depart_signature_line(self, node):
        self.body.append('}')

    def visit_desc_signature(self, node):
        if node.parent['objtype'] != 'describe' and node['ids']:
            hyper = self.hypertarget(node['ids'][0])
        else:
            hyper = ''
        self.body.append(hyper)
        if not node.get('is_multiline'):
            self._visit_signature_line(node)
        else:
            self.body.append('%\n\\pysigstartmultiline\n')

    def depart_desc_signature(self, node):
        if not node.get('is_multiline'):
            self._depart_signature_line(node)
        else:
            self.body.append('%\n\\pysigstopmultiline')

    def visit_desc_signature_line(self, node):
        self._visit_signature_line(node)

    def depart_desc_signature_line(self, node):
        self._depart_signature_line(node)

    def visit_desc_addname(self, node):
        self.body.append(r'\sphinxcode{')
        self.literal_whitespace += 1

    def depart_desc_addname(self, node):
        self.body.append('}')
        self.literal_whitespace -= 1

    def visit_desc_type(self, node):
        pass

    def depart_desc_type(self, node):
        pass

    def visit_desc_returns(self, node):
        self.body.append(r'{ $\rightarrow$ ')

    def depart_desc_returns(self, node):
        self.body.append(r'}')

    def visit_desc_name(self, node):
        self.body.append(r'\sphinxbfcode{')
        self.no_contractions += 1
        self.literal_whitespace += 1

    def depart_desc_name(self, node):
        self.body.append('}')
        self.literal_whitespace -= 1
        self.no_contractions -= 1

    def visit_desc_parameterlist(self, node):
        # close name, open parameterlist
        self.body.append('}{')
        self.first_param = 1

    def depart_desc_parameterlist(self, node):
        # close parameterlist, open return annotation
        self.body.append('}{')

    def visit_desc_parameter(self, node):
        if not self.first_param:
            self.body.append(', ')
        else:
            self.first_param = 0
        if not node.hasattr('noemph'):
            self.body.append(r'\emph{')

    def depart_desc_parameter(self, node):
        if not node.hasattr('noemph'):
            self.body.append('}')

    def visit_desc_optional(self, node):
        self.body.append(r'\sphinxoptional{')

    def depart_desc_optional(self, node):
        self.body.append('}')

    def visit_desc_annotation(self, node):
        self.body.append(r'\sphinxstrong{')

    def depart_desc_annotation(self, node):
        self.body.append('}')

    def visit_desc_content(self, node):
        if node.children and not isinstance(node.children[0], nodes.paragraph):
            # avoid empty desc environment which causes a formatting bug
            self.body.append('~')

    def depart_desc_content(self, node):
        pass

    def visit_seealso(self, node):
        self.body.append(u'\n\n\\sphinxstrong{%s:}\n\n' % admonitionlabels['seealso'])

    def depart_seealso(self, node):
        self.body.append("\n\n")

    def visit_rubric(self, node):
        if len(node.children) == 1 and node.children[0].astext() in \
           ('Footnotes', _('Footnotes')):
            raise nodes.SkipNode
        self.body.append('\\paragraph{')
        self.context.append('}\n')
        self.in_title = 1

    def depart_rubric(self, node):
        self.in_title = 0
        self.body.append(self.context.pop())

    def visit_footnote(self, node):
        raise nodes.SkipNode

    def visit_collected_footnote(self, node):
        self.in_footnote += 1
        if 'footnotetext' in node:
            self.body.append('%%\n\\begin{footnotetext}[%s]'
                             '\\sphinxAtStartFootnote\n' % node['number'])
        else:
            if self.in_parsed_literal:
                self.body.append('\\begin{footnote}[%s]' % node['number'])
            else:
                self.body.append('%%\n\\begin{footnote}[%s]' % node['number'])
            self.body.append('\\sphinxAtStartFootnote\n')

    def depart_collected_footnote(self, node):
        if 'footnotetext' in node:
            self.body.append('%\n\\end{footnotetext}')
        else:
            if self.in_parsed_literal:
                self.body.append('\\end{footnote}')
            else:
                self.body.append('%\n\\end{footnote}')
        self.in_footnote -= 1

    def visit_label(self, node):
        if isinstance(node.parent, nodes.citation):
            self.bibitems[-1][0] = node.astext()
            self.bibitems[-1][2] = self.curfilestack[-1]
            self.bibitems[-1][3] = node.parent['ids'][0]
        raise nodes.SkipNode

    def visit_tabular_col_spec(self, node):
        self.next_table_colspec = node['spec']
        raise nodes.SkipNode

    def visit_table(self, node):
        if self.table:
            raise UnsupportedError(
                '%s:%s: nested tables are not yet implemented.' %
                (self.curfilestack[-1], node.line or ''))
        self.table = Table()
        self.table.longtable = 'longtable' in node['classes']
        self.tablebody = []
        self.tableheaders = []
        # Redirect body output until table is finished.
        self.pushbody(self.tablebody)
        self.restrict_footnote(node)

    def depart_table(self, node):
        if self.table.rowcount > 30:
            self.table.longtable = True
        self.popbody()
        if not self.table.longtable and self.table.caption is not None:
            self.body.append('\n\n\\begin{threeparttable}\n'
                             '\\capstart\\caption{')
            for caption in self.table.caption:
                self.body.append(caption)
            self.body.append('}')
            for id in self.pop_hyperlink_ids('table'):
                self.body.append(self.hypertarget(id, anchor=False))
            if node['ids']:
                self.body.append(self.hypertarget(node['ids'][0], anchor=False))
        if self.table.longtable:
            self.body.append('\n\\begin{longtable}')
            endmacro = '\\end{longtable}\n\n'
        elif self.table.has_verbatim:
            self.body.append('\n\\noindent\\begin{tabular}')
            endmacro = '\\end{tabular}\n\n'
        elif self.table.has_problematic and not self.table.colspec:
            # if the user has given us tabularcolumns, accept them and use
            # tabulary nevertheless
            self.body.append('\n\\noindent\\begin{tabular}')
            endmacro = '\\end{tabular}\n\n'
        else:
            self.body.append('\n\\noindent\\begin{tabulary}{\\linewidth}')
            endmacro = '\\end{tabulary}\n\n'
        if self.table.colspec:
            self.body.append(self.table.colspec)
        else:
            if self.table.has_problematic:
                colspec = ('*{%d}{p{\\dimexpr(\\linewidth-\\arrayrulewidth)/%d'
                           '-2\\tabcolsep-\\arrayrulewidth\\relax}|}' %
                           (self.table.colcount, self.table.colcount))
                self.body.append('{|' + colspec + '}\n')
            elif self.table.longtable:
                self.body.append('{|' + ('l|' * self.table.colcount) + '}\n')
            else:
                self.body.append('{|' + ('L|' * self.table.colcount) + '}\n')
        if self.table.longtable and self.table.caption is not None:
            self.body.append(u'\\caption{')
            for caption in self.table.caption:
                self.body.append(caption)
            self.body.append('}')
            for id in self.pop_hyperlink_ids('table'):
                self.body.append(self.hypertarget(id, anchor=False))
            if node['ids']:
                self.body.append(self.hypertarget(node['ids'][0], anchor=False))
            self.body.append(u'\\\\\n')
        if self.table.longtable:
            self.body.append('\\hline\n')
            self.body.extend(self.tableheaders)
            self.body.append('\\endfirsthead\n\n')
            self.body.append('\\multicolumn{%s}{c}%%\n' % self.table.colcount)
            self.body.append(r'{\makebox[0pt]{\tablecontinued{\tablename\ '
                             r'\thetable{} -- %s}}}\\'
                             % _('continued from previous page'))
            self.body.append('\n\\hline\n')
            self.body.extend(self.tableheaders)
            self.body.append('\\endhead\n\n')
            self.body.append(r'\hline \multicolumn{%s}{|r|}{\makebox[0pt][r]'
                             r'{\tablecontinued{%s}}}\\\hline'
                             % (self.table.colcount,
                                _('Continued on next page')))
            self.body.append('\n\\endfoot\n\n')
            self.body.append('\\endlastfoot\n\n')
        else:
            self.body.append('\\hline\n')
            self.body.extend(self.tableheaders)
        self.body.extend(self.tablebody)
        self.body.append(endmacro)
        if not self.table.longtable and self.table.caption is not None:
            self.body.append('\\end{threeparttable}\n\n')
        self.unrestrict_footnote(node)
        self.table = None
        self.tablebody = None

    def visit_colspec(self, node):
        self.table.colcount += 1

    def depart_colspec(self, node):
        pass

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    def visit_thead(self, node):
        self.table.had_head = True
        if self.next_table_colspec:
            self.table.colspec = '{%s}\n' % self.next_table_colspec
        self.next_table_colspec = None
        # Redirect head output until header is finished. see visit_tbody.
        self.body = self.tableheaders

    def depart_thead(self, node):
        pass

    def visit_tbody(self, node):
        if not self.table.had_head:
            self.visit_thead(node)
        self.body = self.tablebody

    def depart_tbody(self, node):
        self.remember_multirow = {}
        self.remember_multirowcol = {}

    def visit_row(self, node):
        self.table.col = 0
        for key, value in self.remember_multirow.items():
            if not value and key in self.remember_multirowcol:
                del self.remember_multirowcol[key]

    def depart_row(self, node):
        self.body.append('\\\\\n')
        if any(self.remember_multirow.values()):
            linestart = 1
            col = self.table.colcount
            for col in range(1, self.table.col + 1):
                if self.remember_multirow.get(col):
                    if linestart != col:
                        linerange = str(linestart) + '-' + str(col - 1)
                        self.body.append('\\cline{' + linerange + '}')
                    linestart = col + 1
                    if self.remember_multirowcol.get(col, 0):
                        linestart += self.remember_multirowcol[col]
            if linestart <= col:
                linerange = str(linestart) + '-' + str(col)
                self.body.append('\\cline{' + linerange + '}')
        else:
            self.body.append('\\hline')
        self.table.rowcount += 1

    def visit_entry(self, node):
        if self.table.col == 0:
            while self.remember_multirow.get(self.table.col + 1, 0):
                self.table.col += 1
                self.remember_multirow[self.table.col] -= 1
                if self.remember_multirowcol.get(self.table.col, 0):
                    extracols = self.remember_multirowcol[self.table.col]
                    self.body.append('\\multicolumn{')
                    self.body.append(str(extracols + 1))
                    self.body.append('}{|l|}{}\\relax ')
                    self.table.col += extracols
                self.body.append('&')
        else:
            self.body.append('&')
        self.table.col += 1
        context = ''
        if 'morecols' in node:
            self.body.append('\\multicolumn{')
            self.body.append(str(node.get('morecols') + 1))
            if self.table.col == 1:
                self.body.append('}{|l|}{\\relax ')
            else:
                self.body.append('}{l|}{\\relax ')
            context += '\\unskip}\\relax '
        if 'morerows' in node:
            self.body.append('\\multirow{')
            self.body.append(str(node.get('morerows') + 1))
            self.body.append('}{*}{\\relax ')
            context += '\\unskip}\\relax '
            self.remember_multirow[self.table.col] = node.get('morerows')
        if 'morecols' in node:
            if 'morerows' in node:
                self.remember_multirowcol[self.table.col] = node.get('morecols')
            self.table.col += node.get('morecols')
        if (('morecols' in node or 'morerows' in node) and
           (len(node) > 2 or len(node.astext().split('\n')) > 2)):
            self.in_merged_cell = 1
            self.literal_whitespace += 1
            self.body.append('\\eqparbox{%d}{\\vspace{.5\\baselineskip}\n' % id(node))
            self.pushbody([])
            context += '}'
        if isinstance(node.parent.parent, nodes.thead):
            if len(node) == 1 and isinstance(node[0], nodes.paragraph) and node.astext() == '':
                pass
            else:
                self.body.append('\\sphinxstylethead{\\relax ')
                context += '\\unskip}\\relax '
        while self.remember_multirow.get(self.table.col + 1, 0):
            self.table.col += 1
            self.remember_multirow[self.table.col] -= 1
            context += '&'
            if self.remember_multirowcol.get(self.table.col, 0):
                extracols = self.remember_multirowcol[self.table.col]
                context += '\\multicolumn{'
                context += str(extracols + 1)
                context += '}{l|}{}\\relax '
                self.table.col += extracols
        if len(node.traverse(nodes.paragraph)) >= 2:
            self.table.has_problematic = True
        self.context.append(context)

    def depart_entry(self, node):
        if self.in_merged_cell:
            self.in_merged_cell = 0
            self.literal_whitespace -= 1
            body = self.popbody()
            # Remove empty lines from top of merged cell
            while body and body[0] == "\n":
                body.pop(0)
            for line in body:
                line = re.sub(u'(?<!~\\\\\\\\)\n', u'~\\\\\\\\\n', line)  # escape return code
                self.body.append(line)
        self.body.append(self.context.pop())  # header

    def visit_acks(self, node):
        # this is a list in the source, but should be rendered as a
        # comma-separated list here
        self.body.append('\n\n')
        self.body.append(', '.join(n.astext()
                                   for n in node.children[0].children) + '.')
        self.body.append('\n\n')
        raise nodes.SkipNode

    def visit_bullet_list(self, node):
        if not self.compact_list:
            self.body.append('\\begin{itemize}\n')
        if self.table:
            self.table.has_problematic = True

    def depart_bullet_list(self, node):
        if not self.compact_list:
            self.body.append('\\end{itemize}\n')

    def visit_enumerated_list(self, node):
        self.body.append('\\begin{enumerate}\n')
        if 'start' in node:
            self.body.append('\\setcounter{enumi}{%d}\n' % (node['start'] - 1))
        if self.table:
            self.table.has_problematic = True

    def depart_enumerated_list(self, node):
        self.body.append('\\end{enumerate}\n')

    def visit_list_item(self, node):
        # Append "{}" in case the next character is "[", which would break
        # LaTeX's list environment (no numbering and the "[" is not printed).
        self.body.append(r'\item {} ')

    def depart_list_item(self, node):
        self.body.append('\n')

    def visit_definition_list(self, node):
        self.body.append('\\begin{description}\n')
        if self.table:
            self.table.has_problematic = True

    def depart_definition_list(self, node):
        self.body.append('\\end{description}\n')

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass

    def visit_term(self, node):
        self.in_term += 1
        ctx = '}] \\leavevmode'
        if node.get('ids'):
            ctx += self.hypertarget(node['ids'][0])
        self.body.append('\\item[{')
        self.restrict_footnote(node)
        self.context.append(ctx)

    def depart_term(self, node):
        self.body.append(self.context.pop())
        self.unrestrict_footnote(node)
        self.in_term -= 1

    def visit_termsep(self, node):
        warnings.warn('sphinx.addnodes.termsep will be removed at Sphinx-1.6. '
                      'This warning is displayed because some Sphinx extension '
                      'uses sphinx.addnodes.termsep. Please report it to '
                      'author of the extension.', RemovedInSphinx16Warning)
        self.body.append(', ')
        raise nodes.SkipNode

    def visit_classifier(self, node):
        self.body.append('{[}')

    def depart_classifier(self, node):
        self.body.append('{]}')

    def visit_definition(self, node):
        pass

    def depart_definition(self, node):
        self.body.append('\n')

    def visit_field_list(self, node):
        self.body.append('\\begin{quote}\\begin{description}\n')
        if self.table:
            self.table.has_problematic = True

    def depart_field_list(self, node):
        self.body.append('\\end{description}\\end{quote}\n')

    def visit_field(self, node):
        pass

    def depart_field(self, node):
        pass

    visit_field_name = visit_term
    depart_field_name = depart_term

    visit_field_body = visit_definition
    depart_field_body = depart_definition

    def visit_paragraph(self, node):
        index = node.parent.index(node)
        if (index > 0 and isinstance(node.parent, nodes.compound) and
                not isinstance(node.parent[index - 1], nodes.paragraph) and
                not isinstance(node.parent[index - 1], nodes.compound)):
            # insert blank line, if the paragraph follows a non-paragraph node in a compound
            self.body.append('\\noindent\n')
        elif index == 0 and isinstance(node.parent, nodes.footnote):
            # don't insert blank line, if the paragraph is first child of a footnote
            pass
        else:
            self.body.append('\n')

    def depart_paragraph(self, node):
        self.body.append('\n')

    def visit_centered(self, node):
        self.body.append('\n\\begin{center}')
        if self.table:
            self.table.has_problematic = True

    def depart_centered(self, node):
        self.body.append('\n\\end{center}')

    def visit_hlist(self, node):
        # for now, we don't support a more compact list format
        # don't add individual itemize environments, but one for all columns
        self.compact_list += 1
        self.body.append('\\begin{itemize}\\setlength{\\itemsep}{0pt}'
                         '\\setlength{\\parskip}{0pt}\n')
        if self.table:
            self.table.has_problematic = True

    def depart_hlist(self, node):
        self.compact_list -= 1
        self.body.append('\\end{itemize}\n')

    def visit_hlistcol(self, node):
        pass

    def depart_hlistcol(self, node):
        pass

    def latex_image_length(self, width_str):
        try:
            return rstdim_to_latexdim(width_str)
        except ValueError:
            self.builder.warn('dimension unit %s is invalid. Ignored.' % width_str)

    def is_inline(self, node):
        """Check whether a node represents an inline element."""
        return isinstance(node.parent, nodes.TextElement)

    def visit_image(self, node):
        attrs = node.attributes
        pre = []                        # in reverse order
        post = []
        if self.in_parsed_literal:
            pre = ['\\begingroup\\sphinxunactivateextrasandspace\\relax ']
            post = ['\\endgroup ']
        include_graphics_options = []
        is_inline = self.is_inline(node)
        if 'width' in attrs:
            w = self.latex_image_length(attrs['width'])
            if w:
                include_graphics_options.append('width=%s' % w)
        if 'height' in attrs:
            h = self.latex_image_length(attrs['height'])
            if h:
                include_graphics_options.append('height=%s' % h)
        if 'scale' in attrs:
            if include_graphics_options:
                # unfortunately passing "height=1cm,scale=2.0" to \includegraphics
                # does not result in a height of 2cm. We must scale afterwards.
                pre.append('\\scalebox{%f}{' % (attrs['scale'] / 100.0,))
                post.append('}')
            else:
                # if no "width" nor "height", \sphinxincludegraphics will fit
                # to the available text width if oversized after rescaling.
                include_graphics_options.append('scale=%s'
                                                % (float(attrs['scale']) / 100.0))
        if 'align' in attrs:
            align_prepost = {
                # By default latex aligns the top of an image.
                (1, 'top'): ('', ''),
                (1, 'middle'): ('\\raisebox{-0.5\\height}{', '}'),
                (1, 'bottom'): ('\\raisebox{-\\height}{', '}'),
                (0, 'center'): ('{\\hspace*{\\fill}', '\\hspace*{\\fill}}'),
                # These 2 don't exactly do the right thing.  The image should
                # be floated alongside the paragraph.  See
                # http://www.w3.org/TR/html4/struct/objects.html#adef-align-IMG
                (0, 'left'): ('{', '\\hspace*{\\fill}}'),
                (0, 'right'): ('{\\hspace*{\\fill}', '}'),
            }
            try:
                pre.append(align_prepost[is_inline, attrs['align']][0])
                post.append(align_prepost[is_inline, attrs['align']][1])
            except KeyError:
                pass
        if not is_inline:
            pre.append('\n\\noindent')
            post.append('\n')
        pre.reverse()
        if node['uri'] in self.builder.images:
            uri = self.builder.images[node['uri']]
        else:
            # missing image!
            if self.ignore_missing_images:
                return
            uri = node['uri']
        if uri.find('://') != -1:
            # ignore remote images
            return
        self.body.extend(pre)
        options = ''
        if include_graphics_options:
            options = '[%s]' % ','.join(include_graphics_options)
        base, ext = path.splitext(uri)
        if self.in_title and base:
            # Lowercase tokens forcely because some fncychap themes capitalize
            # the options of \sphinxincludegraphics unexpectly (ex. WIDTH=...).
            self.body.append('\\lowercase{\\sphinxincludegraphics%s}{{%s}%s}' %
                             (options, base, ext))
        else:
            self.body.append('\\sphinxincludegraphics%s{{%s}%s}' %
                             (options, base, ext))
        self.body.extend(post)

    def depart_image(self, node):
        pass

    def visit_figure(self, node):
        ids = ''
        for id in self.pop_hyperlink_ids('figure'):
            ids += self.hypertarget(id, anchor=False)
        if node['ids']:
            ids += self.hypertarget(node['ids'][0], anchor=False)
        self.restrict_footnote(node)
        if (len(node.children) and
           isinstance(node.children[0], nodes.image) and
           node.children[0]['ids']):
            ids += self.hypertarget(node.children[0]['ids'][0], anchor=False)
        if self.table:
            # TODO: support align option
            if 'width' in node:
                length = self.latex_image_length(node['width'])
                if length:
                    self.body.append('\\begin{sphinxfigure-in-table}[%s]\n'
                                     '\\centering\n' % length)
            else:
                self.body.append('\\begin{sphinxfigure-in-table}\n\\centering\n')
            if any(isinstance(child, nodes.caption) for child in node):
                self.body.append('\\capstart')
            self.context.append(ids + '\\end{sphinxfigure-in-table}\\relax\n')
        elif node.get('align', '') in ('left', 'right'):
            length = None
            if 'width' in node:
                length = self.latex_image_length(node['width'])
            elif 'width' in node[0]:
                length = self.latex_image_length(node[0]['width'])
            self.body.append('\\begin{wrapfigure}{%s}{%s}\n\\centering' %
                             (node['align'] == 'right' and 'r' or 'l', length or '0pt'))
            self.context.append(ids + '\\end{wrapfigure}\n')
        elif self.in_minipage:
            if ('align' not in node.attributes or
                    node.attributes['align'] == 'center'):
                self.body.append('\n\\begin{center}')
                self.context.append('\\end{center}\n')
            else:
                self.body.append('\n\\begin{flush%s}' % node.attributes['align'])
                self.context.append('\\end{flush%s}\n' % node.attributes['align'])
        else:
            if ('align' not in node.attributes or
                    node.attributes['align'] == 'center'):
                # centering does not add vertical space like center.
                align = '\n\\centering'
                align_end = ''
            else:
                # TODO non vertical space for other alignments.
                align = '\\begin{flush%s}' % node.attributes['align']
                align_end = '\\end{flush%s}' % node.attributes['align']
            self.body.append('\\begin{figure}[%s]%s\n' % (
                self.elements['figure_align'], align))
            if any(isinstance(child, nodes.caption) for child in node):
                self.body.append('\\capstart\n')
            self.context.append(ids + align_end + '\\end{figure}\n')

    def depart_figure(self, node):
        self.body.append(self.context.pop())
        self.unrestrict_footnote(node)

    def visit_caption(self, node):
        self.in_caption += 1
        self.restrict_footnote(node)
        if self.in_container_literal_block:
            self.body.append('\\sphinxSetupCaptionForVerbatim{')
        elif self.in_minipage and isinstance(node.parent, nodes.figure):
            self.body.append('\\captionof{figure}{')
        elif self.table and node.parent.tagname == 'figure':
            self.body.append('\\sphinxfigcaption{')
        else:
            self.body.append('\\caption{')

    def depart_caption(self, node):
        self.body.append('}')
        self.in_caption -= 1
        self.unrestrict_footnote(node)

    def visit_legend(self, node):
        self.body.append('\n\\begin{sphinxlegend}')

    def depart_legend(self, node):
        self.body.append('\\end{sphinxlegend}\n')

    def visit_admonition(self, node):
        self.body.append('\n\\begin{sphinxadmonition}{note}')

    def depart_admonition(self, node):
        self.body.append('\\end{sphinxadmonition}\n')

    def _make_visit_admonition(name):
        def visit_admonition(self, node):
            self.body.append(u'\n\\begin{sphinxadmonition}{%s}{%s:}' %
                             (name, admonitionlabels[name]))
        return visit_admonition

    def _depart_named_admonition(self, node):
        self.body.append('\\end{sphinxadmonition}\n')

    visit_attention = _make_visit_admonition('attention')
    depart_attention = _depart_named_admonition
    visit_caution = _make_visit_admonition('caution')
    depart_caution = _depart_named_admonition
    visit_danger = _make_visit_admonition('danger')
    depart_danger = _depart_named_admonition
    visit_error = _make_visit_admonition('error')
    depart_error = _depart_named_admonition
    visit_hint = _make_visit_admonition('hint')
    depart_hint = _depart_named_admonition
    visit_important = _make_visit_admonition('important')
    depart_important = _depart_named_admonition
    visit_note = _make_visit_admonition('note')
    depart_note = _depart_named_admonition
    visit_tip = _make_visit_admonition('tip')
    depart_tip = _depart_named_admonition
    visit_warning = _make_visit_admonition('warning')
    depart_warning = _depart_named_admonition

    def visit_versionmodified(self, node):
        pass

    def depart_versionmodified(self, node):
        pass

    def visit_target(self, node):
        def add_target(id):
            # indexing uses standard LaTeX index markup, so the targets
            # will be generated differently
            if id.startswith('index-'):
                return
            # do not generate \phantomsection in \section{}
            anchor = not self.in_title
            self.body.append(self.hypertarget(id, anchor=anchor))

        # postpone the labels until after the sectioning command
        parindex = node.parent.index(node)
        try:
            try:
                next = node.parent[parindex + 1]
            except IndexError:
                # last node in parent, look at next after parent
                # (for section of equal level) if it exists
                if node.parent.parent is not None:
                    next = node.parent.parent[
                        node.parent.parent.index(node.parent)]
                else:
                    raise
            if isinstance(next, nodes.section):
                if node.get('refid'):
                    self.next_section_ids.add(node['refid'])
                self.next_section_ids.update(node['ids'])
                return
            else:
                domain = self.builder.env.domains['std']
                figtype = domain.get_figtype(next)
                if figtype and domain.get_numfig_title(next):
                    ids = set()
                    # labels for figures go in the figure body, not before
                    if node.get('refid'):
                        ids.add(node['refid'])
                    ids.update(node['ids'])
                    self.push_hyperlink_ids(figtype, ids)
                    return
        except IndexError:
            pass
        if 'refuri' in node:
            return
        if node.get('refid'):
            add_target(node['refid'])
        for id in node['ids']:
            add_target(id)

    def depart_target(self, node):
        pass

    def visit_attribution(self, node):
        self.body.append('\n\\begin{flushright}\n')
        self.body.append('---')

    def depart_attribution(self, node):
        self.body.append('\n\\end{flushright}\n')

    def visit_index(self, node, scre=re.compile(r';\s*')):
        if not node.get('inline', True):
            self.body.append('\n')
        entries = node['entries']
        for type, string, tid, ismain, key_ in entries:
            m = ''
            if ismain:
                m = '|textbf'
            try:
                if type == 'single':
                    p = scre.sub('!', self.encode(string))
                    self.body.append(r'\index{%s%s}' % (p, m))
                elif type == 'pair':
                    p1, p2 = [self.encode(x) for x in split_into(2, 'pair', string)]
                    self.body.append(r'\index{%s!%s%s}\index{%s!%s%s}' %
                                     (p1, p2, m, p2, p1, m))
                elif type == 'triple':
                    p1, p2, p3 = [self.encode(x)
                                  for x in split_into(3, 'triple', string)]
                    self.body.append(
                        r'\index{%s!%s %s%s}\index{%s!%s, %s%s}'
                        r'\index{%s!%s %s%s}' %
                        (p1, p2, p3, m, p2, p3, p1, m, p3, p1, p2, m))
                elif type == 'see':
                    p1, p2 = [self.encode(x) for x in split_into(2, 'see', string)]
                    self.body.append(r'\index{%s|see{%s}}' % (p1, p2))
                elif type == 'seealso':
                    p1, p2 = [self.encode(x) for x in split_into(2, 'seealso', string)]
                    self.body.append(r'\index{%s|see{%s}}' % (p1, p2))
                else:
                    self.builder.warn(
                        'unknown index entry type %s found' % type)
            except ValueError as err:
                self.builder.warn(str(err))
        raise nodes.SkipNode

    def visit_raw(self, node):
        if 'latex' in node.get('format', '').split():
            self.body.append(node.astext())
        raise nodes.SkipNode

    def visit_reference(self, node):
        if not self.in_title:
            for id in node.get('ids'):
                anchor = not self.in_caption
                self.body += self.hypertarget(id, anchor=anchor)
        uri = node.get('refuri', '')
        if not uri and node.get('refid'):
            uri = '%' + self.curfilestack[-1] + '#' + node['refid']
        if self.in_title or not uri:
            self.context.append('')
        elif uri.startswith('#'):
            # references to labels in the same document
            id = self.curfilestack[-1] + ':' + uri[1:]
            self.body.append(self.hyperlink(id))
            self.body.append(r'\emph{')
            if self.builder.config.latex_show_pagerefs and not \
                    self.in_production_list:
                self.context.append('}}} (%s)' % self.hyperpageref(id))
            else:
                self.context.append('}}}')
        elif uri.startswith('%'):
            # references to documents or labels inside documents
            hashindex = uri.find('#')
            if hashindex == -1:
                # reference to the document
                id = uri[1:] + '::doc'
            else:
                # reference to a label
                id = uri[1:].replace('#', ':')
            self.body.append(self.hyperlink(id))
            if len(node) and hasattr(node[0], 'attributes') and \
               'std-term' in node[0].get('classes', []):
                # don't add a pageref for glossary terms
                self.context.append('}}}')
                # mark up as termreference
                self.body.append(r'\sphinxtermref{')
            else:
                self.body.append(r'\sphinxcrossref{')
                if self.builder.config.latex_show_pagerefs and not \
                   self.in_production_list:
                    self.context.append('}}} (%s)' % self.hyperpageref(id))
                else:
                    self.context.append('}}}')
        else:
            if len(node) == 1 and uri == node[0]:
                if node.get('nolinkurl'):
                    self.body.append('\\sphinxnolinkurl{%s}' % self.encode_uri(uri))
                else:
                    self.body.append('\\sphinxurl{%s}' % self.encode_uri(uri))
                raise nodes.SkipNode
            else:
                self.body.append('\\sphinxhref{%s}{' % self.encode_uri(uri))
                self.context.append('}')

    def depart_reference(self, node):
        self.body.append(self.context.pop())

    def visit_number_reference(self, node):
        if node.get('refid'):
            id = self.curfilestack[-1] + ':' + node['refid']
        else:
            id = node.get('refuri', '')[1:].replace('#', ':')

        title = node.get('title', '%s')
        title = text_type(title).translate(tex_escape_map).replace('\\%s', '%s')
        if '\\{name\\}' in title or '\\{number\\}' in title:
            # new style format (cf. "Fig.%{number}")
            title = title.replace('\\{name\\}', '{name}').replace('\\{number\\}', '{number}')
            text = escape_abbr(title).format(name='\\nameref{%s}' % self.idescape(id),
                                             number='\\ref{%s}' % self.idescape(id))
        else:
            # old style format (cf. "Fig.%{number}")
            text = escape_abbr(title) % ('\\ref{%s}' % self.idescape(id))
        hyperref = '\\hyperref[%s]{%s}' % (self.idescape(id), text)
        self.body.append(hyperref)

        raise nodes.SkipNode

    def visit_download_reference(self, node):
        pass

    def depart_download_reference(self, node):
        pass

    def visit_pending_xref(self, node):
        pass

    def depart_pending_xref(self, node):
        pass

    def visit_emphasis(self, node):
        self.body.append(r'\sphinxstyleemphasis{')

    def depart_emphasis(self, node):
        self.body.append('}')

    def visit_literal_emphasis(self, node):
        self.body.append(r'\sphinxstyleliteralemphasis{')
        self.no_contractions += 1

    def depart_literal_emphasis(self, node):
        self.body.append('}')
        self.no_contractions -= 1

    def visit_strong(self, node):
        self.body.append(r'\sphinxstylestrong{')

    def depart_strong(self, node):
        self.body.append('}')

    def visit_literal_strong(self, node):
        self.body.append(r'\sphinxstyleliteralstrong{')
        self.no_contractions += 1

    def depart_literal_strong(self, node):
        self.body.append('}')
        self.no_contractions -= 1

    def visit_abbreviation(self, node):
        abbr = node.astext()
        self.body.append(r'\sphinxstyleabbreviation{')
        # spell out the explanation once
        if node.hasattr('explanation') and abbr not in self.handled_abbrs:
            self.context.append('} (%s)' % self.encode(node['explanation']))
            self.handled_abbrs.add(abbr)
        else:
            self.context.append('}')

    def depart_abbreviation(self, node):
        self.body.append(self.context.pop())

    def visit_manpage(self, node):
        return self.visit_literal_emphasis(node)

    def depart_manpage(self, node):
        return self.depart_literal_emphasis(node)

    def visit_title_reference(self, node):
        self.body.append(r'\sphinxtitleref{')

    def depart_title_reference(self, node):
        self.body.append('}')

    def visit_citation(self, node):
        # TODO maybe use cite bibitems
        # bibitem: [citelabel, citetext, docname, citeid]
        self.bibitems.append(['', '', '', ''])
        self.context.append(len(self.body))

    def depart_citation(self, node):
        size = self.context.pop()
        text = ''.join(self.body[size:])
        del self.body[size:]
        self.bibitems[-1][1] = text

    def visit_citation_reference(self, node):
        # This is currently never encountered, since citation_reference nodes
        # are already replaced by pending_xref nodes in the environment.
        self.body.append('\\cite{%s}' % self.idescape(node.astext()))
        raise nodes.SkipNode

    def visit_literal(self, node):
        self.no_contractions += 1
        if self.in_title:
            self.body.append(r'\sphinxstyleliteralintitle{')
        else:
            self.body.append(r'\sphinxcode{')

    def depart_literal(self, node):
        self.no_contractions -= 1
        self.body.append('}')

    def visit_footnote_reference(self, node):
        num = node.astext().strip()
        try:
            footnode, used = self.footnotestack[-1][num]
        except (KeyError, IndexError):
            raise nodes.SkipNode
        # if a footnote has been inserted once, it shouldn't be repeated
        # by the next reference
        if used:
            self.body.append('\\sphinxfootnotemark[%s]' % num)
        elif self.footnote_restricted:
            self.footnotestack[-1][num][1] = True
            self.body.append('\\sphinxfootnotemark[%s]' % num)
            self.pending_footnotes.append(footnode)
        else:
            self.footnotestack[-1][num][1] = True
            footnode.walkabout(self)
        raise nodes.SkipChildren

    def depart_footnote_reference(self, node):
        pass

    def visit_literal_block(self, node):
        if node.rawsource != node.astext():
            # most probably a parsed-literal block -- don't highlight
            self.in_parsed_literal += 1
            self.body.append('\\begin{sphinxalltt}\n')
        else:
            ids = ''
            for id in self.pop_hyperlink_ids('code-block'):
                ids += self.hypertarget(id, anchor=False)
            if node['ids']:
                # suppress with anchor=False \phantomsection insertion
                ids += self.hypertarget(node['ids'][0], anchor=False)
            # LaTeX code will insert \phantomsection prior to \label
            if ids and not self.in_footnote:
                self.body.append('\n\\def\\sphinxLiteralBlockLabel{' + ids + '}')
            code = node.astext()
            lang = self.hlsettingstack[-1][0]
            linenos = code.count('\n') >= self.hlsettingstack[-1][1] - 1
            highlight_args = node.get('highlight_args', {})
            if 'language' in node:
                # code-block directives
                lang = node['language']
                highlight_args['force'] = True
            if 'linenos' in node:
                linenos = node['linenos']
            if lang is self.hlsettingstack[0][0]:
                # only pass highlighter options for original language
                opts = self.builder.config.highlight_options
            else:
                opts = {}

            def warner(msg, **kwargs):
                self.builder.warn(msg, (self.curfilestack[-1], node.line), **kwargs)
            hlcode = self.highlighter.highlight_block(code, lang, opts=opts,
                                                      warn=warner, linenos=linenos,
                                                      **highlight_args)
            # workaround for Unicode issue
            hlcode = hlcode.replace(u'€', u'@texteuro[]')
            if self.in_footnote:
                self.body.append('\n\\sphinxSetupCodeBlockInFootnote')
                hlcode = hlcode.replace('\\begin{Verbatim}',
                                        '\\begin{sphinxVerbatim}')
            # if in table raise verbatim flag to avoid "tabulary" environment
            # and opt for sphinxVerbatimintable to handle caption & long lines
            elif self.table:
                self.table.has_problematic = True
                self.table.has_verbatim = True
                hlcode = hlcode.replace('\\begin{Verbatim}',
                                        '\\begin{sphinxVerbatimintable}')
            else:
                hlcode = hlcode.replace('\\begin{Verbatim}',
                                        '\\begin{sphinxVerbatim}')
            # get consistent trailer
            hlcode = hlcode.rstrip()[:-14]  # strip \end{Verbatim}
            if self.table and not self.in_footnote:
                hlcode += '\\end{sphinxVerbatimintable}'
            else:
                hlcode += '\\end{sphinxVerbatim}'
            self.body.append('\n' + hlcode + '\n')
            if ids:
                self.body.append('\\let\\sphinxLiteralBlockLabel\\empty\n')
            raise nodes.SkipNode

    def depart_literal_block(self, node):
        self.body.append('\n\\end{sphinxalltt}\n')
        self.in_parsed_literal -= 1
    visit_doctest_block = visit_literal_block
    depart_doctest_block = depart_literal_block

    def visit_line(self, node):
        self.body.append('\item[] ')

    def depart_line(self, node):
        self.body.append('\n')

    def visit_line_block(self, node):
        if isinstance(node.parent, nodes.line_block):
            self.body.append('\\item[]\n'
                             '\\begin{DUlineblock}{\\DUlineblockindent}\n')
        else:
            self.body.append('\n\\begin{DUlineblock}{0em}\n')
        if self.table:
            self.table.has_problematic = True

    def depart_line_block(self, node):
        self.body.append('\\end{DUlineblock}\n')

    def visit_block_quote(self, node):
        # If the block quote contains a single object and that object
        # is a list, then generate a list not a block quote.
        # This lets us indent lists.
        done = 0
        if len(node.children) == 1:
            child = node.children[0]
            if isinstance(child, nodes.bullet_list) or \
                    isinstance(child, nodes.enumerated_list):
                done = 1
        if not done:
            self.body.append('\\begin{quote}\n')
            if self.table:
                self.table.has_problematic = True

    def depart_block_quote(self, node):
        done = 0
        if len(node.children) == 1:
            child = node.children[0]
            if isinstance(child, nodes.bullet_list) or \
                    isinstance(child, nodes.enumerated_list):
                done = 1
        if not done:
            self.body.append('\\end{quote}\n')

    # option node handling copied from docutils' latex writer

    def visit_option(self, node):
        if self.context[-1]:
            # this is not the first option
            self.body.append(', ')

    def depart_option(self, node):
        # flag that the first option is done.
        self.context[-1] += 1

    def visit_option_argument(self, node):
        """The delimiter betweeen an option and its argument."""
        self.body.append(node.get('delimiter', ' '))

    def depart_option_argument(self, node):
        pass

    def visit_option_group(self, node):
        self.body.append('\\item [')
        # flag for first option
        self.context.append(0)

    def depart_option_group(self, node):
        self.context.pop()  # the flag
        self.body.append('] ')

    def visit_option_list(self, node):
        self.body.append('\\begin{optionlist}{3cm}\n')
        if self.table:
            self.table.has_problematic = True

    def depart_option_list(self, node):
        self.body.append('\\end{optionlist}\n')

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        pass

    def visit_option_string(self, node):
        ostring = node.astext()
        self.no_contractions += 1
        self.body.append(self.encode(ostring))
        self.no_contractions -= 1
        raise nodes.SkipNode

    def visit_description(self, node):
        self.body.append(' ')

    def depart_description(self, node):
        pass

    def visit_superscript(self, node):
        self.body.append('$^{\\text{')

    def depart_superscript(self, node):
        self.body.append('}}$')

    def visit_subscript(self, node):
        self.body.append('$_{\\text{')

    def depart_subscript(self, node):
        self.body.append('}}$')

    def visit_substitution_definition(self, node):
        raise nodes.SkipNode

    def visit_substitution_reference(self, node):
        raise nodes.SkipNode

    def visit_inline(self, node):
        classes = node.get('classes', [])
        if classes in [['menuselection'], ['guilabel']]:
            self.body.append(r'\sphinxmenuselection{')
            self.context.append('}')
        elif classes in [['accelerator']]:
            self.body.append(r'\sphinxaccelerator{')
            self.context.append('}')
        elif classes and not self.in_title:
            self.body.append(r'\DUrole{%s}{' % ','.join(classes))
            self.context.append('}')
        else:
            self.context.append('')

    def depart_inline(self, node):
        self.body.append(self.context.pop())

    def visit_generated(self, node):
        pass

    def depart_generated(self, node):
        pass

    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

    def visit_container(self, node):
        if node.get('literal_block'):
            self.in_container_literal_block += 1
            ids = ''
            for id in self.pop_hyperlink_ids('code-block'):
                ids += self.hypertarget(id, anchor=False)
            if node['ids']:
                # suppress with anchor=False \phantomsection insertion
                ids += self.hypertarget(node['ids'][0], anchor=False)
            # define label for use in caption.
            if ids:
                self.body.append('\n\\def\\sphinxLiteralBlockLabel{' + ids + '}\n')

    def depart_container(self, node):
        if node.get('literal_block'):
            self.in_container_literal_block -= 1
            self.body.append('\\let\\sphinxVerbatimTitle\\empty\n')
            self.body.append('\\let\\sphinxLiteralBlockLabel\\empty\n')

    def visit_decoration(self, node):
        pass

    def depart_decoration(self, node):
        pass

    # docutils-generated elements that we don't support

    def visit_header(self, node):
        raise nodes.SkipNode

    def visit_footer(self, node):
        raise nodes.SkipNode

    def visit_docinfo(self, node):
        raise nodes.SkipNode

    # text handling

    def encode(self, text):
        text = text_type(text).translate(tex_escape_map)
        if self.literal_whitespace:
            # Insert a blank before the newline, to avoid
            # ! LaTeX Error: There's no line here to end.
            text = text.replace(u'\n', u'~\\\\\n').replace(u' ', u'~')
        if self.no_contractions:
            text = text.replace('--', u'-{-}')
            text = text.replace("''", u"'{'}")
        return text

    def encode_uri(self, text):
        # in \href, the tilde is allowed and must be represented literally
        return self.encode(text).replace('\\textasciitilde{}', '~')

    def visit_Text(self, node):
        text = self.encode(node.astext())
        if not self.no_contractions and not self.in_parsed_literal:
            text = educate_quotes_latex(text,
                                        dquotes=("\\sphinxquotedblleft{}",
                                                 "\\sphinxquotedblright{}"))
        self.body.append(text)

    def depart_Text(self, node):
        pass

    def visit_comment(self, node):
        raise nodes.SkipNode

    def visit_meta(self, node):
        # only valid for HTML
        raise nodes.SkipNode

    def visit_system_message(self, node):
        pass

    def depart_system_message(self, node):
        self.body.append('\n')

    def visit_math(self, node):
        self.builder.warn('using "math" markup without a Sphinx math extension '
                          'active, please use one of the math extensions '
                          'described at http://sphinx-doc.org/ext/math.html',
                          (self.curfilestack[-1], node.line))
        raise nodes.SkipNode

    visit_math_block = visit_math

    def unknown_visit(self, node):
        raise NotImplementedError('Unknown node: ' + node.__class__.__name__)
