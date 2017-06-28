# -*- coding: utf-8 -*-
# Copyright (c) 2013 Tomasz Wójcik <tomek@bthlabs.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import sys
from email import utils

SEMISPACE = '; '


def encoded(_str, coding):
    if sys.version_info[0] == 3:
        return _str
    else:
        if isinstance(_str, unicode):
            return _str.encode(coding)
        else:
            return _str


def _py2_formatparam(param, value=None, quote=True):
    """ Fixed version of email.message._formatparam.
    Python 3 has fixed the bug to be RFC compliant.

    This will quote the value if needed or if quote is true.  If value is a
    three tuple (charset, language, value), it will be encoded according
    to RFC2231 rules.  If it contains non-ascii characters it will likewise
    be encoded according to RFC2231 rules, using the utf-8 charset and
    a null language.
    """
    if value is not None and len(value) > 0:
        # A tuple is used for RFC 2231 encoded parameter values where items
        # are (charset, language, value).  charset is a string, not a Charset
        # instance.  RFC 2231 encoded values are never quoted, per RFC.
        if isinstance(value, tuple):
            # Encode as per RFC 2231
            param += '*'
            value = utils.encode_rfc2231(value[2], value[0], value[1])
            return '%s=%s' % (param, value)
        else:
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                param += '*'
                value = utils.encode_rfc2231(value, 'utf-8', '')
                return '%s=%s' % (param, value)
        # BAW: Please check this.  I think that if quote is set it should
        # force quoting even if not necessary.
        if quote or tspecials.search(value):
            return '%s="%s"' % (param, utils.quote(value))
        else:
            return '%s=%s' % (param, value)
    else:
        return param


def _py2_add_header(msg_part, _name, _value, **_params):
    """Extended header setting.

    name is the header field to add.  keyword arguments can be used to set
    additional parameters for the header field, with underscores converted
    to dashes.  Normally the parameter will be added as key="value" unless
    value is None, in which case only the key will be added.  If a
    parameter value contains non-ASCII characters it can be specified as a
    three-tuple of (charset, language, value), in which case it will be
    encoded according to RFC2231 rules.  Otherwise it will be encoded using
    the utf-8 charset and a language of ''.

    Examples:

    msg.add_header('content-disposition', 'attachment', filename='bud.gif')
    msg.add_header('content-disposition', 'attachment',
                   filename=('utf-8', '', Fußballer.ppt'))
    msg.add_header('content-disposition', 'attachment',
                   filename='Fußballer.ppt'))
    """
    parts = []
    for k, v in _params.items():
        if v is None:
            parts.append(k.replace('_', '-'))
        else:
            parts.append(_py2_formatparam(k.replace('_', '-'), v))
    if _value is not None:
        parts.insert(0, _value)
    msg_part._headers.append((_name, SEMISPACE.join(parts)))


def add_header(msg_part, _name, _value, **_params):
    if sys.version_info[0] == 3:
        msg_part.add_header(_name, _value, **_params)
    else:
        _py2_add_header(msg_part, _name, _value, **_params)
