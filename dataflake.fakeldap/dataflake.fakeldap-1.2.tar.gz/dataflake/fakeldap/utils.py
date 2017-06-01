##############################################################################
#
# Copyright (c) 2012 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from base64 import b64encode
from hashlib import sha1 as sha_new
import ldap.dn
import six


def hash_pwd(pwd_str):
    if isinstance(pwd_str, six.text_type):
        pwd_str = pwd_str.encode('utf-8')
    sha_digest = sha_new(pwd_str).digest()
    return '{SHA}%s' % b64encode(sha_digest).strip()


def explode_dn(dn):
    parts = []
    raw_parts = ldap.dn.explode_dn(dn)
    for part in raw_parts:
        if six.PY2 and isinstance(part, six.text_type):
            part = part.encode('UTF-8')
        parts.append(part)
    return parts
