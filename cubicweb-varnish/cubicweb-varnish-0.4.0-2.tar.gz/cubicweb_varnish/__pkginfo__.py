# pylint: disable=W0622
"""cubicweb-varnish application packaging information"""

modname = 'cubicweb_varnish'
distname = 'cubicweb-varnish'

numversion = (0, 4, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL-2.1'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'cubicweb varnish helper'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.24.0',
    'six': None,
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]
