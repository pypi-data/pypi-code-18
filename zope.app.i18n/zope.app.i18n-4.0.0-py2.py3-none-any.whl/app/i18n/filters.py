##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Translation Domain Message Export and Import Filters

"""
__docformat__ = 'restructuredtext'

import time
import re

from zope.interface import implementer

from zope.i18n.interfaces import IMessageExportFilter, IMessageImportFilter
from zope.app.i18n.interfaces import ILocalTranslationDomain

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)

class ParseError(Exception):
    def __init__(self, state, lineno, line=''):
        Exception.__init__(self, state, lineno, line)
        self.state = state
        self.lineno = lineno
        self.line = line

    def __str__(self):
        return "state %s, line num %s: '%s'" % (self.state, self.lineno, self.line)

def _find_language(languages, kind):
    if isinstance(languages, string_types):
        languages = [languages]

    if len(languages) != 1:
        raise TypeError(
            'Exactly one language at a time is supported for gettext %s.' % (kind,))

    return languages[0]


@implementer(IMessageExportFilter)
class GettextExportFilter(object):

    __used_for__ = ILocalTranslationDomain


    def __init__(self, domain):
        self.domain = domain

    def exportMessages(self, languages):
        'See IMessageExportFilter'
        domain = self.domain.domain

        language = _find_language(languages, 'export')

        dt = time.time()
        dt = time.localtime(dt)
        dt = time.strftime('%Y/%m/%d %H:%M', dt)
        if not isinstance(dt, bytes):
            dt = dt.encode('utf-8')
        output = _file_header % (dt, language.encode('UTF-8'),
                                 domain.encode('UTF-8'))

        for msgid in sorted(self.domain.getMessageIds()):
            msgstr = self.domain.translate(msgid, target_language=language)
            msgstr = msgstr.encode('UTF-8')
            msgid = msgid.encode('UTF-8')
            output += _msg_template % (msgid, msgstr)

        return output


@implementer(IMessageImportFilter)
class GettextImportFilter(object):

    __used_for__ = ILocalTranslationDomain

    def __init__(self, domain):
        self.domain = domain

    def importMessages(self, languages, data_file):
        'See IMessageImportFilter'

        language = _find_language(languages, 'import')

        result = parseGetText(data_file.readlines())[3]
        headers = parserHeaders(b''.join(result[(b'',)][1]))
        del result[(b'',)]
        charset = extractCharset(headers[b'content-type'])
        for msg in result.items():
            msgid = b''.join(msg[0]).decode(charset)
            msgid = msgid.replace('\\n', '\n')
            msgstr = b''.join(msg[1][1]).decode(charset)
            msgstr = msgstr.replace('\\n', '\n')
            self.domain.addMessage(msgid, msgstr, language)



def extractCharset(header):
    charset = header.split(b'charset=')[-1]
    if not isinstance(charset, str):
        charset = charset.decode('utf-8')
    return charset.lower()


def parserHeaders(headers_bytes):
    headers = {}
    for line in headers_bytes.split(b'\\n'):
        name = line.split(b':')[0]
        value = b''.join(line.split(b':')[1:])
        headers[name.lower()] = value

    return headers


def parseGetText(content):
    # The regular expressions
    com = re.compile(b'^#.*')
    msgid = re.compile(br'^ *msgid *"(.*?[^\\]*)"')
    msgstr = re.compile(br'^ *msgstr *"(.*?[^\\]*)"')
    re_str = re.compile(br'^ *"(.*?[^\\])"')
    blank = re.compile(br'^\s*$')

    trans = {}
    pointer = 0
    state = 0
    COM, MSGID, MSGSTR = [], [], []
    while pointer < len(content):
        line = content[pointer]
        #print 'STATE:', state
        #print 'LINE:', line, content[pointer].strip()
        if state == 0:
            COM, MSGID, MSGSTR = [], [], []
            if com.match(line):
                COM.append(line.strip())
                state = 1
                pointer = pointer + 1
            elif msgid.match(line):
                MSGID.append(msgid.match(line).group(1))
                state = 2
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise ParseError(0, pointer + 1, line)
        elif state == 1:
            if com.match(line):
                COM.append(line.strip())
                state = 1
                pointer = pointer + 1
            elif msgid.match(line):
                MSGID.append(msgid.match(line).group(1))
                state = 2
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise ParseError(1, pointer + 1, line)

        elif state == 2:
            if com.match(line):
                COM.append(line.strip())
                state = 2
                pointer = pointer + 1
            elif re_str.match(line):
                MSGID.append(re_str.match(line).group(1))
                state = 2
                pointer = pointer + 1
            elif msgstr.match(line):
                MSGSTR.append(msgstr.match(line).group(1))
                state = 3
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise ParseError(2, pointer + 1, line)

        elif state == 3:
            if com.match(line) or msgid.match(line):
                # print "\nEn", language, "detected", MSGID
                trans[tuple(MSGID)] = (COM, MSGSTR)
                state = 0
            elif re_str.match(line):
                MSGSTR.append(re_str.match(line).group(1))
                state = 3
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise ParseError(3, pointer + 1, line)

    # the last also goes in
    if tuple(MSGID):
        trans[tuple(MSGID)] = (COM, MSGSTR)

    return COM, MSGID, MSGSTR, trans


_file_header = b'''
msgid ""
msgstr ""
"Project-Id-Version: Zope 3\\n"
"PO-Revision-Date: %s\\n"
"Last-Translator: Zope 3 Gettext Export Filter\\n"
"Zope-Language: %s\\n"
"Zope-Domain: %s\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
'''

_msg_template = b'''
msgid "%s"
msgstr "%s"
'''
